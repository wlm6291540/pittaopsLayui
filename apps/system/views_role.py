import json

from django.db.models import Q
from django.db.models.functions import Lower, Concat
from django.forms import model_to_dict, modelformset_factory
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView

from system.forms import MenuUpdateForm, RoleForm
from system.models import Menu, Role, User
from utils.Paginator import paginate
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, ListView

# Create your views here.
from system.models import Menu


class RoleMainView(TemplateView):
    template_name = 'system/role.html'


class RoleCreateView(CreateView):
    model = Role
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        code = 1
        msg = '添加失败'
        form = self.get_form()
        if form.is_valid():
            form.save()
            code = 0
            msg = '添加成功'
        print(form.is_valid())
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class RoleListView(View):
    def get(self, request):
        code = 1
        msg = '获取失败'
        total = 0
        result = []
        try:
            code = 0
            msg = '获取成功'
            fields = ['id', 'name', 'desc']
            data = Role.objects.values(*fields)
            total = len(data)
            result = paginate(request, data)
        except Exception as e:
            msg = str(e)
        ret = dict(code=code, msg=msg, count=total, data=result)
        return JsonResponse(ret)


class RoleDeleteView(DeleteView):
    def post(self, request):
        code, msg = 0, "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            role = Role.objects.filter(id__in=data)
            role.delete()
        else:
            code, msg = 1, "删除失败"
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class RoleUpdateView(View):
    def post(self, request):
        code, msg = 0, '更新成功'
        try:
            role = Role.objects.get(id=request.POST.get('id', None))
            if role:
                form = RoleForm(request.POST)
                form.is_valid()
                form.instance.id = role.id
                form.instance.save()
            else:
                raise ValueError('id 为{}的角色不存在'.format(id))
        except ValueError as e:
            code, msg = 1, str(e)
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class RoleBindUserView(View):
    def get(self, request):
        code, msg = 0, '用户获取成功'
        data = None
        try:
            roleid = request.GET.get('roleid', None)
            inrole = request.GET.get('inrole', None)
            fields = ['id', 'username', 'nickname']
            if roleid is not None and inrole is not None:
                role = Role.objects.get(id=int(roleid))
                if inrole == 'false':
                    data = list(User.objects.values(*fields).filter(~Q(role=role)).all())
                elif inrole == 'true':
                    data = list(User.objects.values(*fields).filter(role=role).all())
            else:
                data = list(User.objects.values(*fields).all())
        except User.DoesNotExist as e:
            print(e)
            code, msg = 1, 'id 为{}的角色不存在'.format(roleid)
        ret = dict(code=code, msg=msg, data=data)
        return JsonResponse(ret)

    def post(self, request):
        code, msg = 0, '角色关联成功'
        try:
            ids = json.loads(request.POST.get('ids'))
            roleid = request.POST.get('roleid')
            if ids and roleid:
                role = Role.objects.get(id=int(roleid))
                user = User.objects.filter(id__in=ids).all()
                role.user_set.set(user)
                role.save()
            elif len(ids) <= 0 and roleid:
                role = Role.objects.get(id=int(roleid))
                role.user_set.set([])
                role.save()
            else:
                code = 1
                msg = '关联失败'
        except Role.DoesNotExist as e:
            print(e)
            code, msg = 1, '系统内部错误'
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class RoleMenuTreeView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        result = []
        param = request.GET
        roleid = param.get('roleid', None)
        select = param.get('select', None)
        fields = ['id', 'name', 'parent']
        for item in Menu.objects.filter(parent=None):
            second = []
            for item2 in Menu.objects.filter(parent=item):
                tmp = list(Menu.objects.filter(parent=item2).values(*fields, title=Lower('name')))
                data = model_to_dict(item2)
                second.append({**data, 'title': data['name'], 'children': tmp})
            tmp = model_to_dict(item)
            result.append({**tmp, 'title': tmp['name'], 'children': second})
        return JsonResponse(result, safe=False)
