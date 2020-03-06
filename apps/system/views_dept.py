import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from system.models import Department

# Create your views here.


class DepartmentMainView(TemplateView):
    template_name = 'system/dept.html'


class DepartmentListView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        fields = ['id', 'name', 'type', 'parent', 'parent__name']
        data = list(Department.objects.values(*fields).all())
        for item in data:
            if item['type'] == 'unit':
                item['type'] = '单位'
            else:
                item['type'] = '部门'
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')
