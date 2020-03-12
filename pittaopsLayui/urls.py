"""pittaopsLayui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from system.urls import system_urls
from system.views import MainPageView
from system.views_user import ImageUploadView

urlpatterns = [
    path('', MainPageView.as_view(), name='main page'),
    path('index', MainPageView.as_view(), name='index page'),
    path('upload', ImageUploadView.as_view(), name='upload'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend(system_urls)