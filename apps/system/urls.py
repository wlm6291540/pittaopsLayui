from django.urls import path

from system.views_dept import (
    DepartmentMainView, DepartmentListView, DepartmentTreeView, DepartmentCreateView, DepartmentDeleteView,
    DepartmentUpdateView, DepartmentBindUserView)
from system.views_menu import MenuMainView, MenuListView, MenuTreeView, MenuCreateView, MenuUpdateView, MenuDeleteView

from system.views_user import (
    UserMainView, UserListView, UserCreateView, UserDeleteView,
    UserUpdateView, UserActiveView)

from system.view_perm import (
    PermissionMainView)

from system.views_role import (
    RoleMainView)

system_urls = []

# 部门url
dept_url = [
    path('system/dept', DepartmentMainView.as_view(), name='dept main'),
    path('system/dept/list', DepartmentListView.as_view(), name='dept list'),
    path('system/dept/tree', DepartmentTreeView.as_view(), name='dept tree'),
    path('system/dept/create', DepartmentCreateView.as_view(), name='dept create'),
    path('system/dept/delete', DepartmentDeleteView.as_view(), name='dept delete'),
    path('system/dept/update', DepartmentUpdateView.as_view(), name='dept update'),
    path('system/dept/binduser', DepartmentBindUserView.as_view(), name='dept bind user')
]

# 角色url
role_url = [
    path('system/role', RoleMainView.as_view(), name='role main')
]

# 用户url
user_url = [
    path('system/user', UserMainView.as_view(), name='user main'),
    path('system/user/list', UserListView.as_view(), name='user list'),
    path('system/user/create', UserCreateView.as_view(), name='user create'),
    path('system/user/delete', UserDeleteView.as_view(), name='user delete'),
    path('system/user/update', UserUpdateView.as_view(), name='user update'),
    path('system/user/active', UserActiveView.as_view(), name='user active'),
]

# 权限url
perm_url = [
    path('system/perm', PermissionMainView.as_view(), name='perm main')
]

# 菜单url
menu_url = [
    path('system/menu', MenuMainView.as_view(), name='menu main'),
    path('system/menu/list', MenuListView.as_view(), name='menu list'),
    path('system/menu/create', MenuCreateView.as_view(), name='menu create'),
    path('system/menu/delete', MenuDeleteView.as_view(), name='menu delete'),
    path('system/menu/update', MenuUpdateView.as_view(), name='menu update'),
    path('system/menu/tree', MenuTreeView.as_view(), name='menu tree'),
]

system_urls.extend(dept_url)
system_urls.extend(role_url)
system_urls.extend(user_url)
system_urls.extend(perm_url)
system_urls.extend(menu_url)
