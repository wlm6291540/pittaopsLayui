from django.db.models.functions import Lower
from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from system.models import Menu


class CmdbMainPageView(TemplateView):
    template_name = 'cmdb/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        roles = list(user.role.all())
        menus = []
        for role in roles:
            menus.append(list(role.permissions.values()))
        menus = to_tree(None, Menu, 1, menus=menus)
        context['menus'] = menus
        return context


def to_tree(parent, model, level=1, fields=['id', 'name', 'url'], menus=[]):
    result = []
    for item in model.objects.filter(parent=parent):
        data = model_to_dict(item, fields=fields)
        if level > 4:
            break
        elif level < 4:
            if level > 2 and item.id in menus:
                pass
            data['children'] = to_tree(item, model, level + 1, menus=menus)
        else:
            tmp = []
            for item2 in model.objects.filter(parent=item).values(*fields, label=Lower('name')):
                if item2['id'] in menus:
                    tmp.append(item2)
            data['children'] = tmp
        result.append(data)
    return result