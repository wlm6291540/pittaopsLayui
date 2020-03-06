from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class UserMainView(TemplateView):
    template_name = 'system/user.html'
