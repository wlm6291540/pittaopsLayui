import datetime
import hashlib
import json
import os
import random
import re

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q

# Create your views here.
from system.forms import UserCreateForm, UserUpdateForm
from system.models import Department
from utils.JsonEncoder import DatetimeJsonEncoder

# image location
User = get_user_model()


class LoginPageView(TemplateView):
    template_name = 'login.html'


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(dict(code=0, msg='登录成功'))
        else:
            return JsonResponse(dict(code=1, msg='用户名或密码错误'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("login")


class UserMainView(TemplateView):
    template_name = 'system/user.html'


class UserListView(View):
    def get(self, request):
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        post = param.get('post', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        code = 0
        msg = '获取成功'
        fields = ['id', 'username', 'nickname', 'email', 'avatar', 'is_active', 'post',
                  'superior', 'department', 'department__name']
        if post:
            data = list(User.objects.values(*fields).filter(post=post))
        else:
            data = list(User.objects.values(*fields))[(page - 1) * limit:page * limit]
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserCreateView(View):
    def post(self, request):
        code = 1
        msg = ''
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.password = make_password(user_form.cleaned_data['password'])
            new_user.save()
            user_form.save_m2m()
            code = 0
            msg = '添加成功'
        else:
            pattern = '<li>(.*?)<ul class=.*?><li>(.*?)</li>'
            errors = re.findall(pattern, str(user_form.errors))
            for error in errors:
                msg += '{}: {}\n'.format(*error)
        ret = dict(code=code, msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDeleteView(View):
    def post(self, request):
        code = 0
        message = "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            print(type(data), data)
            if 1 in data:
                data.pop(data.index(1))
            user = User.objects.filter(id__in=data).all()
            user.delete()
        else:
            code = 1
            message = "删除失败"
        ret = dict(code=code, msg=message)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserUpdateView(View):
    def post(self, request):
        code = 1
        msg = '修改失败'
        # try:
        data = request.POST
        user = User.objects.get(id=data.get('id'))
        if user:
            dept_id = data.get('department', None)
            superior_id = data.get('superior', None)
            is_active = data.get('is_active', None)
            password = data.get('password', None)
            department = Department.objects.get(id=dept_id) if dept_id else None
            superior = User.objects.get(id=superior_id) if superior_id else None
            user.nickname = data.get('nickname', None)
            user.email = data.get('email', None)
            user.avatar = data.get('avatar', None)
            user.department = department
            user.post = data.get('post', None)
            user.superior = superior
            if not user.is_superuser:
                user.is_active = True if is_active == '1' else False
            if password and len(password) > 6:
                user.password = make_password(password)
            user.save()
            code = 0
            msg = '修改成功'
        else:
            code = 1
            msg = '该用户不存在'

        # except Exception as e:
        #     code = 1
        #     msg = '系统内部错误'
        #     print(e)
        ret = dict(code=code, msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserActiveView(View):
    def post(self, request):
        code = 0
        msg = ''
        ids = request.POST.get('ids', None)
        status = request.POST.get('status', None)
        if ids:
            data = json.loads(ids)
            if status == 'true':
                status = 1
                msg = '启用成功'
            else:
                status = 0
                msg = '禁用成功'
            if 1 in data:
                data.pop(data.index(1))
            user = User.objects.filter(id__in=data).update(is_active=status)
        else:
            code = 1
            msg = '参数错误'
        ret = dict(code=code, msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class ImageUploadView(View):
    def post(self, request):
        code = 0
        msg = '上传成功'
        data = None
        try:
            image = request.FILES['file']
            # 需要判断文件类型是否是图片.
            name = image.name
            image = Image.open(image)
            w, h = image.size
            if w >= h:
                w_start = (w - h) * 0.618
                box = (w_start, 0, w_start + h, h)
                region = image.crop(box)
            else:
                h_start = (h - w) * 0.618
                box = (0, h_start, w, h_start + w)
                region = image.crop(box)

            location = str(name).find('.')
            extension = name[location:]

            name = name[:location] + str(datetime.datetime.now()) + str(random.random())
            md5 = hashlib.md5(name.encode('utf-8')).hexdigest()
            image.name = md5[:10] + extension
            with open(os.path.join(settings.MEDIA_ROOT) + '/avatar/' + image.name, 'w') as file:
                image.save(file)
            data = {'url': settings.MEDIA_URL + 'avatar/' + image.name}
        except Exception as e:
            code = 1
            msg = '系统内部错误'
            print(e)
        ret = dict(code=code, msg=msg, data=data)
        return JsonResponse(ret)
