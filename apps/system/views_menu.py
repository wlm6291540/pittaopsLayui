import json

from django.db.models.functions import Lower, Concat
from django.forms import model_to_dict, modelformset_factory
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView

from system.forms import MenuUpdateForm
from system.models import Menu
from utils.Paginator import paginate


class MenuMainView(TemplateView):
    template_name = 'system/menu.html'


class MenuCreateView(CreateView):
    model = Menu
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


class MenuListView(View):
    def get(self, request):
        code = 1
        msg = '获取失败'
        total = 0
        result = []
        try:
            code = 0
            msg = '获取成功'
            fields = ['id', 'name', 'code', 'icon', 'url', 'parent', 'parent__name']
            data = Menu.objects.values(*fields)
            total = len(data)
            result = paginate(request, data)
        except Exception as e:
            msg = str(e)
        ret = dict(code=code, msg=msg, count=total, data=result)
        return JsonResponse(ret)


class MenuTreeView(View):
    def get(self, request):
        code = 0
        msg = '获取成功'
        result = []
        fields = ['id', 'name', 'parent']
        for item in Menu.objects.filter(parent=None):
            second = []
            for item2 in Menu.objects.filter(parent=item):
                tmp = list(Menu.objects.filter(parent=item2).values(*fields, label=Lower('name')))
                data = model_to_dict(item2)
                second.append({**data, 'label': data['name'], 'children': tmp})
            tmp = model_to_dict(item)
            result.append({**tmp, 'label': tmp['name'], 'children': second})
        return JsonResponse(result, safe=False)


class MenuDeleteView(DeleteView):
    def post(self, request):
        code, msg = 0, "删除成功"
        data = request.POST.get('ids', None)
        if data:
            data = json.loads(data)
            menu = Menu.objects.filter(id__in=data)
            menu.delete()
        else:
            code, msg = 1, "删除失败"
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)


class MenuUpdateView(View):
    def post(self, request):
        code, msg = 0, '更新成功'
        try:
            old_menu = Menu.objects.get(id=request.POST.get('id', None))
            if old_menu:
                menu_form = MenuUpdateForm(request.POST)
                menu_form.is_valid()
                menu_form.instance.id = old_menu.id
                menu_form.instance.save()
            else:
                raise ValueError('id 为{}的菜单不存在'.format(id))
        except ValueError as e:
            code, msg = 1, str(e)
        ret = dict(code=code, msg=msg)
        return JsonResponse(ret)
