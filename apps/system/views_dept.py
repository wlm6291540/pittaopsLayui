import json

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View


from system.models import Department, User


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


class DepartmentUpdateView(View):
    def post(self, request):
        code = 0
        msg = "修改成功"
        data = json.loads(request.body)
        try:
            dept = Department.objects.get(id=int(data['id']))
            dept.type = data['type']
            dept.name = data['name']
            if dept:
                if data['parent'] is None and data['type'] == 'unit':
                    dept.save()
                elif (data['parent'] is None or len(data['parent']) < 1) and data['type'] != 'unit':
                    code = 1
                    msg = "不能创建没有上级单位的部门"
                elif data['parent'] and data['type'] == 'unit':
                    code = 1
                    msg = "不能创建有上级部门的单位"
                else:
                    pdept = None
                    if len(data['parent']) > 0:
                        pdept = Department.objects.get(id=data['parent'])
                    if len(Department.objects.filter(name=data['name'], type=data['type'], parent=pdept).all()) < 1:
                        dept.parent = pdept
                        dept.save()
                    else:
                        code = 1
                        message = "存在同名的部门"
            else:
                code = 1
                msg = '不能存在该部门'
        except ValueError as e:
            code = 1
            msg = "系统内部错误"
        ret = dict(code=code, msg=msg)
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


class DepartmentBindUserView(View):
    def get(self, request):
        code, msg = 0, '用户获取成功'
        data = None
        try:
            deptid = request.GET.get('deptid', None)
            indept = request.GET.get('indept', None)
            fields = ['id', 'username', 'nickname']
            if deptid is not None and indept is not None:
                dept = Department.objects.get(id=int(deptid))
                if indept == 'false':
                    data = list(User.objects.values(*fields).filter(~Q(department=dept)).all())
                elif indept == 'true':
                    data = list(User.objects.values(*fields).filter(department=dept).all())
            else:
                data = list(User.objects.values(*fields).all())
        except Department.DoesNotExist as e:
            print(e)
            code, msg = 1, 'id 为{}的部门不存在'.format(deptid)
        ret = dict(code=code, msg=msg, data=data)
        return HttpResponse(json.dumps(ret), content_type='application/json')

    def post(self, request):
        code, msg = 0, '部门关联成功'
        try:
            ids = json.loads(request.POST.get('ids'))
            deptid = request.POST.get('deptid')
            deptid = int(deptid)
            if ids and deptid:
                dept = Department.objects.get(id=deptid)
                User.objects.filter(id__in=ids).update(department=dept)
            elif len(ids) <= 0 and deptid:
                dept = Department.objects.get(id=deptid)
                User.objects.filter(department=dept).update(department=None)
        except Department.DoesNotExist as e:
            print(e)
            code, msg = 1, '系统内部错误'
        ret = dict(code=code, msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')

