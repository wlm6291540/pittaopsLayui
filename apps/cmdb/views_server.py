import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from cmdb.forms import ServerForm, ServerUpdateForm
from cmdb.models import Server, IDC


def get_fix_number():
    return 'ZC' + str(datetime.now().year) + str(datetime.now().month) + \
    str(datetime.now().day) + str(datetime.now().second) + str(int(random.random() * 1000))


class ServerMainView(TemplateView):
    template_name = 'cmdb/server.html'


class ServerListView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        fields = ['id', 'name', 'fix_number', 'manager', 'public_ip', 'private_ip',
                  'idc', 'idc__name', 'adder', 'adder__username', 'add_time']
        data = list(Server.objects.values(*fields)[(page - 1) * limit:page * limit])
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return JsonResponse(ret)


class ServerCreateView(CreateView):
    model = Server
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        code = 1
        msg = '添加失败'
        form = ServerForm(request.POST)
        form.instance.add_time = datetime.now()
        form.instance.fix_number = get_fix_number()
        form.instance.adder = request.user
        form.instance.idc = IDC.objects.get(id=int(request.POST.get('idc')))
        if form.is_valid():
            form.instance.save()
            code = 0
            msg = '添加成功'
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class ServerUpdateView(View):
    def post(self, request):
        code, msg = 0, '更新成功'
        try:
            old_server = Server.objects.get(id=request.POST.get('id', None))
            if old_server:
                form = ServerUpdateForm(request.POST)
                form.is_valid()
                old_server.name = form.instance.name
                old_server.manager = form.instance.manager
                old_server.public_ip = form.instance.public_ip
                old_server.private_ip = form.instance.private_ip
                old_server.idc = form.instance.idc
                old_server.save()
            else:
                raise ValueError('id 为{}server'.format(id))
        except ValueError as e:
            code, msg = 1, str(e)
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class ServerDeleteView(View):
    def post(self, request):
        code, msg = 0, "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            idc = Server.objects.filter(id__in=data)
            idc.delete()
        else:
            code, msg = 1, "删除失败"
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)
