from datetime import datetime

from django.db import models

# Create your models here.
from system.models import User


class IDC(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name='机房名')
    area = models.CharField(max_length=32, blank=True, null=False, verbose_name='区域')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')


class Server(models.Model):
    public_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name='公网IP')
    private_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name='公网IP')
    manager = models.CharField(max_length=255, blank=True, null=True, verbose_name='管理地址')
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name='名称')
    idc = models.ForeignKey(IDC, related_name='server', on_delete=models.DO_NOTHING, verbose_name='机房')
    fix_number = models.CharField(max_length=64, blank=False, null=False, verbose_name='资产编号')
    add_time = models.DateTimeField(default=datetime.now(), verbose_name='添加时间')
    adder = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='添加人')


class Group(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True, verbose_name='分组名')
    desc = models.CharField(max_length=32, null=False, blank=False, verbose_name='备注')


class Label(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True, verbose_name='标签名')
    desc = models.CharField(max_length=32, null=False, blank=False, verbose_name='备注')


class Host(models.Model):
    hostname = models.CharField(max_length=32, null=False, verbose_name='主机名')
    status = models.CharField(max_length=32, null=False, verbose_name='状态')
    public_ip = models.CharField(max_length=64, null=True, verbose_name='公网ip')
    private_ip = models.CharField(max_length=64, null=True, verbose_name='私网ip')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='负责人')
    server = models.ForeignKey(Server, on_delete=models.DO_NOTHING, verbose_name='宿主机')
    os = models.CharField(max_length=64, null=False, default='Linux', verbose_name='操作系统')
    expire = models.DateTimeField(null=True, verbose_name='到期时间')
    type = models.CharField(max_length=64, null=True, verbose_name='类型: 云服务器, 虚拟机')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, verbose_name='分组')
    label = models.ManyToManyField(Label, related_name='host', null=True, verbose_name='标签')


class App(models.Model):
    name = models.CharField(max_length=64, null=False, verbose_name='应用名')
    path = models.CharField(max_length=255, null=False, verbose_name='应用路径')
    port = models.CharField(max_length=64, null=True, verbose_name='端口')
    cmd = models.CharField(max_length=255, null=False, verbose_name='命令')
    config = models.CharField(max_length=255, null=True, verbose_name='配置文件')
    log = models.CharField(max_length=255, null=True, verbose_name='日志')
    start = models.CharField(max_length=255, null=False, verbose_name='启动')
    stop = models.CharField(max_length=255, null=False, verbose_name='停止')
    restart = models.CharField(max_length=255, null=False, verbose_name='重启')
    add_time = models.DateTimeField(default=datetime.now(), verbose_name='添加时间')
    adder = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='添加人')

