from django.urls import path

from cmdb.views import CmdbMainPageView
from cmdb.views_app import AppMainView, AppListView
from cmdb.views_group import GroupMainView, GroupListView, GroupCreateView, GroupDeleteView, GroupUpdateView
from cmdb.views_host import HostMainView, HostListView, HostCreateView, HostDeleteView, HostUpdateView
from cmdb.views_idc import IdcListView, IdcMainView, IdcCreateView, IdcDeleteView, IdcUpdateView
from cmdb.views_label import LabelMainView, LabelListView, LabelCreateView, LabelDeleteView, LabelUpdateView
from cmdb.views_server import ServerMainView, ServerListView, ServerCreateView, ServerDeleteView, ServerUpdateView

cmdb_urls = [
    path('cmdb/view', CmdbMainPageView.as_view(), name='cmdb view'),

    # idc
    path('cmdb/idc/view', IdcMainView.as_view(), name='idc view'),
    path('cmdb/idc/list', IdcListView.as_view(), name='idc list'),
    path('cmdb/idc/create', IdcCreateView.as_view(), name='idc create'),
    path('cmdb/idc/delete', IdcDeleteView.as_view(), name='idc delete'),
    path('cmdb/idc/update', IdcUpdateView.as_view(), name='idc update'),

    # server
    path('cmdb/server/view', ServerMainView.as_view(), name='server view'),
    path('cmdb/server/list', ServerListView.as_view(), name='server list'),
    path('cmdb/server/create', ServerCreateView.as_view(), name='server create'),
    path('cmdb/server/delete', ServerDeleteView.as_view(), name='server delete'),
    path('cmdb/server/update', ServerUpdateView.as_view(), name='server update'),

    # host
    path('cmdb/host/view', HostMainView.as_view(), name='host view'),
    path('cmdb/host/list', HostListView.as_view(), name='host list'),
    path('cmdb/host/create', HostCreateView.as_view(), name='host create'),
    path('cmdb/host/delete', HostDeleteView.as_view(), name='host delete'),
    path('cmdb/host/update', HostUpdateView.as_view(), name='host update'),

    # group
    path('cmdb/group/view', GroupMainView.as_view(), name='group view'),
    path('cmdb/group/list', GroupListView.as_view(), name='group list'),
    path('cmdb/group/create', GroupCreateView.as_view(), name='group create'),
    path('cmdb/group/delete', GroupDeleteView.as_view(), name='group delete'),
    path('cmdb/group/update', GroupUpdateView.as_view(), name='group update'),

    # label
    path('cmdb/label/view', LabelMainView.as_view(), name='label view'),
    path('cmdb/label/list', LabelListView.as_view(), name='label list'),
    path('cmdb/label/create', LabelCreateView.as_view(), name='label create'),
    path('cmdb/label/delete', LabelDeleteView.as_view(), name='label delete'),
    path('cmdb/label/update', LabelUpdateView.as_view(), name='label update'),

    # app
    path('cmdb/app/view', AppMainView.as_view(), name='app view'),
    path('cmdb/app/list', AppListView.as_view(), name='app list'),
    # path('cmdb/app/create', AppCreateView.as_view(), name='app create'),
    # path('cmdb/app/delete', AppDeleteView.as_view(), name='app delete'),
    # path('cmdb/app/update', AppUpdateView.as_view(), name='app update'),
]