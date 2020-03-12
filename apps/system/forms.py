import re

from django.contrib.auth import get_user_model
from django import forms

from system.models import Menu

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    password2 = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "确认密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    class Meta:
        model = User
        fields = [
            'username', 'nickname', 'email', 'avatar', 'department',
            'post', 'superior', 'is_active', 'password', 'password2'
        ]

        error_messages = {
            "username": {"required": "用户名不能为空"},
            "password": {"required": "密码不能为空"},
            "email": {"required": "邮箱不能为空"},
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'nickname', 'email', 'avatar', 'department',
            'post', 'superior', 'is_active', 'password'
        ]

        error_messages = {
            "username": {"required": "用户名不能为空"},
            "email": {"required": "邮箱不能为空"},
        }


class MenuUpdateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'url', 'code', 'icon', 'parent'
        ]

        error_messages = {
            "name": {"required": "菜单名不能为空", 'unique': '菜单名重复'},
        }
