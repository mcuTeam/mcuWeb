# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('system', '0013_terminal_capalityname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='name',
            field=models.IntegerField(unique=True, verbose_name='E164 Alias*'),
        ),
    ]
