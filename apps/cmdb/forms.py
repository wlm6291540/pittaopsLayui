from django.forms import ModelForm

from cmdb.models import IDC, Server, Host, Group, Label


class IdcUpdateForm(ModelForm):
    class Meta:
        model = IDC
        fields = [
            'id', 'name', 'area', 'desc'
        ]

        error_messages = {
            "name": {"required": "idc名不能为空", 'unique': 'idc名重复'},
        }


class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'manager', 'public_ip', 'private_ip']

        error_messages = {
            "name": {"required": "server名不能为空", 'unique': 'server名重复'},
            "private_ip" : {"required": "私有地址不能为空", "unique": "私有地址不能重复"}
        }


class ServerUpdateForm(ModelForm):
    class Meta:
        model = Server
        fields = ['id', 'name', 'manager', 'public_ip', 'private_ip', 'idc']

        error_messages = {
            "name": {"required": "server名不能为空", 'unique': 'server名重复'},
            "private_ip": {"required": "私有地址不能为空", "unique": "私有地址不能重复"}
        }


class HostForm(ModelForm):
    class Meta:
        model = Host
        fields = ['hostname', 'status', 'private_ip', 'owner', 'server', 'os', 'type']

        error_messages = {
            "hostname": {"required": "server名不能为空", 'unique': 'server名重复'},
            "private_ip" : {"required": "私有地址不能为空", "unique": "私有地址不能重复"}
        }


class HostUpdateForm(ModelForm):
    class Meta:
        model = Host
        fields = ['id', 'hostname', 'status', 'private_ip', 'owner', 'server', 'os', 'type', 'expire']
        error_messages = {
            "hostname": {"required": "server名不能为空", 'unique': 'server名重复'},
            "private_ip": {"required": "私有地址不能为空", "unique": "私有地址不能重复"}
        }

class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'desc'
        ]

        error_messages = {
            "name": {"required": "分组名不能为空", 'unique': '分组名重复'},
        }


class LabelUpdateForm(ModelForm):
    class Meta:
        model = Label
        fields = [
            'id', 'name', 'desc'
        ]

        error_messages = {
            "name": {"required": "Label名不能为空", 'unique': 'Label名重复'},
        }