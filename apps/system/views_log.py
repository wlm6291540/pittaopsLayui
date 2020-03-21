import json

from django.db.models import Q
from django.db.models.functions import Lower, Concat
from django.forms import model_to_dict, modelformset_factory
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView

from system.forms import MenuUpdateForm, LoginLogUpdateForm
from system.models import LoginLog
from utils.Paginator import paginate


class LoginLogMainView(TemplateView):
    template_name = 'system/log/login.html'


class LoginLogListView(View):
    def get(self, request):
        code = 1
        msg = '获取失败'
        total = 0
        result = []
        try:
            code = 0
            msg = '获取成功'
            fields = ['id', 'user', 'user__username', 'type', 'ip', 'status', 'login_time']
            data = LoginLog.objects.values(*fields)
            total = len(data)
            result = paginate(request, data)
        except Exception as e:
            msg = str(e)
        ret = dict(code=code, msg=msg, count=total, data=result)
        return JsonResponse(ret)


class LoginLogSearchView(View):
    def post(self, request):
        code = 1
        msg = '搜索失败'
        total = 0
        result = []
        try:
            code = 0
            msg = '获取成功'
            data = request.POST.get('data', None)
            fields = ['id', 'user', 'user__username', 'type', 'ip', 'status', 'login_time']
            data = LoginLog.objects.filter(Q(user__username__contains=data) | Q(ip__contains=data)).values(*fields)
            total = len(data)
            result = paginate(request, data)
        except Exception as e:
            msg = str(e)
        ret = dict(code=code, msg=msg, count=total, data=result)
        return JsonResponse(ret)