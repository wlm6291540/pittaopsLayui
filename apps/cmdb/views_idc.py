import json

from django.db.models.functions import Lower
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from cmdb.forms import IdcUpdateForm
from cmdb.models import IDC
from system.models import Menu


class IdcMainView(TemplateView):
    template_name = 'cmdb/idc.html'


class IdcListView(View):
    def get(self, request):
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        code = 0
        msg = '获取成功'
        data = list(IDC.objects.values()[(page - 1) * limit:page * limit])
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return JsonResponse(ret)


class IdcCreateView(CreateView):
    model = IDC
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        code = 1
        msg = '添加失败'
        form = self.get_form()
        if form.is_valid():
            form.save()
            code = 0
            msg = '添加成功'
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class IdcUpdateView(View):
    def post(self, request):
        code, msg = 0, '更新成功'
        try:
            old_idc = IDC.objects.get(id=request.POST.get('id', None))
            if old_idc:
                form = IdcUpdateForm(request.POST)
                form.is_valid()
                form.instance.id = old_idc.id
                form.instance.save()
            else:
                raise ValueError('id 为{}的idc不存在'.format(id))
        except ValueError as e:
            code, msg = 1, str(e)
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class IdcDeleteView(View):
    def post(self, request):
        code, msg = 0, "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            idc = IDC.objects.filter(id__in=data)
            idc.delete()
        else:
            code, msg = 1, "删除失败"
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)
