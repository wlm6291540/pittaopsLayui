# Generated by Django 3.0.4 on 2020-03-21 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_auto_20200319_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 11, 50, 29, 838586), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='server',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 11, 50, 29, 835363), verbose_name='添加时间'),
        ),
    ]
