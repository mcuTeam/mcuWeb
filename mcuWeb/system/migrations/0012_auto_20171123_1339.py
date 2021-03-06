# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_auto_20171123_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='dualBandWidth',
            field=models.IntegerField(default=1024, verbose_name='双流带宽*'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='videoFrameRate',
            field=models.IntegerField(default=60, verbose_name='视频刷新率*'),
        ),
    ]
