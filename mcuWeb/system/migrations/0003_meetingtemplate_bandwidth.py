# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_meetingtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingtemplate',
            name='bandwidth',
            field=models.CharField(default='4M', max_length=200, verbose_name='bandwidth'),
        ),
    ]
