# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('reciver', models.CharField(max_length=20)),
                ('raddress', models.CharField(max_length=100)),
                ('zipCode', models.CharField(max_length=6)),
                ('rphone', models.CharField(max_length=11)),
            ],
        ),
    ]
