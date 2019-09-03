# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(default='', to='df_goods.TypeInfo'),
        ),
    ]
