# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='raddress',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='reciver',
            field=models.CharField(max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='rphone',
            field=models.CharField(max_length=11, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='zipCode',
            field=models.CharField(max_length=6, default=''),
        ),
    ]
