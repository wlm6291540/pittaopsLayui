# Generated by Django 3.0.4 on 2020-03-13 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_auto_20200311_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='system.Menu', verbose_name='url权限'),
        ),
    ]
