from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith("/login") and not request.user.is_authenticated:
            return render(request, "login.html")


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.username == 'AnonymousUser':
            return
        elif request.path.endswith('/'):
            return
        elif 'logout' in request.path or 'login' in request.path:
            return
        elif 'static' in request.path:
            return
        roles = list(user.role.all())
        menus = []
        for role in roles:
            menus.extend([url['url'] for url in list(role.permissions.values('url'))])
        if 'page' in request.path and request.path not in menus:
            return render(request, '404.html')
        elif request.path not in menus:
            return HttpResponse(status=403)
