from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class PermissionMainView(TemplateView):
    template_name = 'system/perm.html'
