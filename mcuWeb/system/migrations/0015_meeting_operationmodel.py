# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0014_auto_20171127_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='operationModel',
            field=models.CharField(default='操作员模式', max_length=200, verbose_name='操作模式*'),
        ),
    ]
