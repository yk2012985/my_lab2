# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-04 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opertion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsubscribe',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opertion.LessonPublic', verbose_name='预约实验'),
        ),
    ]