# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_auto_20171120_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='audioProtocol',
            field=models.CharField(default='G.711-ulaw', max_length=200, verbose_name='音频协议*'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='bandwidth',
            field=models.CharField(default='4000', max_length=200, verbose_name='带宽*'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='capalityname',
            field=models.CharField(default='1080P', max_length=200, verbose_name='视频分辨率*'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='videoFrameRate',
            field=models.IntegerField(default=60, verbose_name='视频刷新率*'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='videoProtocol',
            field=models.CharField(default='H.264', max_length=200, verbose_name='视频协议*'),
        ),
    ]
