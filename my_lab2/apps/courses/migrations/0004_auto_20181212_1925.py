# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-12 19:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_lesson_detail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessonresource',
            options={'verbose_name': '实验资料', 'verbose_name_plural': '实验资料'},
        ),
    ]