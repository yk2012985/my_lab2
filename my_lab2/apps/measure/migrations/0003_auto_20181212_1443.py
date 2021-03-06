# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-12 14:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0002_auto_20181115_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, verbose_name='实验台编号')),
                ('available', models.BooleanField(default=True, verbose_name='是否可用')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='购买时间')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measure.Laboratory', verbose_name='所属实验室')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='available',
            field=models.BooleanField(default=True, verbose_name='是否可用'),
        ),
        migrations.AlterField(
            model_name='device',
            name='laboratory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measure.Desk', verbose_name='所属实验台'),
        ),
    ]
