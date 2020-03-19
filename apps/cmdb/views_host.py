import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from cmdb.forms import HostForm, HostUpdateForm
from cmdb.models import Host, IDC, Group, Label


def get_fix_number():
    return 'ZC' + str(datetime.now().year) + str(datetime.now().month) + \
    str(datetime.now().day) + str(datetime.now().second) + str(int(random.random() * 1000))


class HostMainView(TemplateView):
    template_name = 'cmdb/host.html'


class HostListView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        fields = ['id', 'hostname', 'status', 'public_ip', 'private_ip', 'owner', 'owner__username',
                  'server', 'server__name', 'os', 'expire', 'type', 'group', 'group__name', 'label', 'label__name']
        data = list(Host.objects.values(*fields)[(page - 1) * limit:page * limit])
        ret = dict(code=code, data=data, count=len(data), msg=msg)
        return JsonResponse(ret)


class HostCreateView(CreateView):
    model = Host
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        code = 1
        msg = '添加失败'
        form = HostForm(request.POST)
        print(form)
        if form.is_valid():
            form.instance.save()
            code = 0
            msg = '添加成功'
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class HostUpdateView(View):
    def post(self, request):
        code, msg = 0, '更新成功'
        #try:
        host = Host.objects.get(id=request.POST.get('id', None))
        if host:
            form = HostUpdateForm(request.POST)
            form.is_valid()
            host.hostname = form.instance.hostname
            host.public_ip = form.instance.public_ip
            host.private_ip = form.instance.private_ip
            host.server = form.instance.server
            host.os = form.instance.os
            host.status = form.instance.status
            host.type = form.instance.type
            if request.POST.get('group', None):
                host.group = Group.objects.get(id=int(request.POST.get('group', None)))
            if request.POST.get('label', None):
                host.label = Label.objects.get(id=int(request.POST.get('label', None)))
            host.expire = form.instance.expire
            host.owner = form.instance.owner
            host.save()
        else:
            raise ValueError('id 为{}Host'.format(id))
        #except ValueError as e:
        #    code, msg = 1, str(e)
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class HostDeleteView(View):
    def post(self, request):
        code, msg = 0, "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            idc = Host.objects.filter(id__in=data)
            idc.delete()
        else:
            code, msg = 1, "删除失败"
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)
