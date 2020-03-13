# Generated by Django 3.0.4 on 2020-03-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_auto_20200313_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='permissions',
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='system.Menu', verbose_name='URL授权'),
        ),
    ]
