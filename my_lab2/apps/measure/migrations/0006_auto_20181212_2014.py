# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-12 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0005_auto_20181212_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='desk',
            name='column',
            field=models.IntegerField(blank=True, null=True, verbose_name='竖排'),
        ),
        migrations.AddField(
            model_name='desk',
            name='row',
            field=models.IntegerField(blank=True, null=True, verbose_name='横排'),
        ),
    ]
