# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-13 14:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0006_auto_20181212_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='desk',
            options={'verbose_name': '实验台', 'verbose_name_plural': '实验台'},
        ),
    ]
