# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-10 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_member_check_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='check_assigned',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Check'),
        ),
    ]
