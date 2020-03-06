from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class RoleMainView(TemplateView):
    template_name = 'system/role.html'
