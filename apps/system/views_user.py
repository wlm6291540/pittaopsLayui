import json

from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q


# Create your views here.
from system.models import Department
from utils.JsonEncoder import DatetimeJsonEncoder

User = get_user_model()

class UserMainView(TemplateView):
    template_name = 'system/user.html'


class UserListView(View):
    def get(self, request):
        param = request.GET
        page = param.get('page', None)
        limit = param.get('limit', None)
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        code = 0
        msg = '获取成功'
        fields = ['id', 'username', 'nickname', 'post', 'superior', 'department', 'department__name']
        data = list(User.objects.values(*fields))
        ret = dict(code=code, data=data[(page - 1) * limit:page*limit], count=len(data), msg=msg)
        return HttpResponse(json.dumps(ret), content_type='application/json')


