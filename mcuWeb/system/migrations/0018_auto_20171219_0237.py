# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_auto_20171205_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='E164 Alias*'),
        ),
    ]