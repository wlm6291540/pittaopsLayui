# Generated by Django 3.0.4 on 2020-03-11 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20200311_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='头像'),
        ),
    ]
