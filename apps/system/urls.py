from django.urls import path

from system.views_dept import (
    DepartmentMainView, DepartmentListView, DepartmentTreeView, DepartmentCreateView, DepartmentDeleteView
)

from system.views_user import (
    UserMainView
)

from system.view_perm import (
    PermissionMainView
)

from system.views_role import (
    RoleMainView
)

system_urls = []

# 部门url
dept_url = [
    path('system/dept', DepartmentMainView.as_view(), name='dept main'),
    path('system/dept/list', DepartmentListView.as_view(), name='dept list'),
    path('system/dept/tree', DepartmentTreeView.as_view(), name='dept tree'),
    path('system/dept/create', DepartmentCreateView.as_view(), name='dept create'),
    path('system/dept/delete', DepartmentDeleteView.as_view(), name='dept delete')
]

# 角色url
role_url = [
    path('system/role', RoleMainView.as_view(), name='role main')
]

# 用户url
user_url = [
    path('system/user', UserMainView.as_view(), name='user main')
]

# 权限url
perm_url = [
    path('system/perm', PermissionMainView.as_view(), name='perm main')
]

system_urls.extend(dept_url)
system_urls.extend(role_url)
system_urls.extend(user_url)
system_urls.extend(perm_url)
