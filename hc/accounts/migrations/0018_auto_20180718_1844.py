# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20180718_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_scheduler',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]