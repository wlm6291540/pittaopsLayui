from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView

# Create your views here.
from system.models import Menu


class RoleMainView(TemplateView):
    template_name = 'system/role.html'


