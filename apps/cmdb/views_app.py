import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, CreateView

from cmdb.models import App


class AppMainView(TemplateView):
    template_name = 'cmdb/app.html'


class AppListView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        fields = ['id', 'name', 'cmd', 'config', 'port',
                  'log', 'start', 'stop', 'restart', 'add_time', 'adder', 'adder__username']
        data = list(App.objects.values(*fields)[(page - 1) * limit:page * limit])
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return JsonResponse(ret)