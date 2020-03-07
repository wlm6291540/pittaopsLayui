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
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        code = 0
        msg = '获取成功'
        fields = ['id', 'name', 'type', 'parent', 'parent__name']
        data = list(Department.objects.values(*fields))
        for item in data:
            if item['type'] == 'unit':
                item['type'] = '单位'
            else:
                item['type'] = '部门'
        ret = dict(code=code, data=data[(page - 1) * limit:page*limit], count=len(data), msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class DepartmentTreeView(View):
    def get(self, request):
        data = []
        fields = ['id', 'name', 'parent']
        topDept = Department.objects.values(*fields).filter(parent=None).all()
        for dept in topDept:
            dept['label'] = dept['name']
            children = list(Department.objects.values(*fields).filter(parent=Department.objects.get(id=dept["id"])))
            for child in children:
                child['label'] = child['name']
            data.append({**dept, "children": children})
        return HttpResponse(json.dumps(data), content_type="application/json")


class DepartmentCreateView(View):
    def get(self, request):
        ret = dict(result=True, departments=Department.objects.all())
        return render(request, 'user/department/add.html', ret)

    def post(self, request):
        status = True
        message = "添加成功"
        data = request.POST
        pid = data.get('parent', None)
        dtype = data.get('type', None)
        name = data.get('name', None)
        try:
            if pid is None and dtype == 'unit':
                if len(Department.objects.filter(name=name, type=dtype).all()) < 1:
                    dept = Department(name=name, type=dtype)
                    dept.save()
                else:
                    status = False
                    message = "存在同名的单位"
            elif (pid is None or len(pid) < 1) and dtype != 'unit':
                status = False
                message = "不能创建没有上级单位的部门"
            elif pid and dtype == 'unit':
                status = False
                message = "不能创建有上级部门的单位"
            else:
                pdept = None
                if len(pid) > 0:
                    pdept = Department.objects.get(id=pid)
                if len(Department.objects.filter(name=name, type=dtype, parent=pdept).all()) < 1:
                    dept = Department(name=name, type=dtype, parent=pdept)
                    dept.save()
                else:
                    status = False
                    message = "存在同名的部门"
        except ValueError as e:
            status = False
            message = "系统内部错误"
        ret = dict(result=status, msg=message)
        print(ret)
        return HttpResponse(json.dumps(ret), content_type="application/json")


class DepartmentDeleteView(View):
    def post(self, request):
        code = 0
        message = "删除成功"
        data = request.POST.get('ids', None)
        print(data)
        if data:
            data = json.loads(data)
            dept = Department.objects.filter(id__in=data)
            dept.delete()
        else:
            code = 1
            message = "删除失败"
        ret = dict(code=code, msg=message)
        return HttpResponse(json.dumps(ret), content_type='application/json')
