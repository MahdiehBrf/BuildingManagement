# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 15:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='resident',
        ),
        migrations.RemoveField(
            model_name='paybyaccount',
            name='account',
        ),
        migrations.RemoveField(
            model_name='paybyaccount',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='paybybank',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='paybybank',
            name='resident',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='resident',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='PayByAccount',
        ),
        migrations.DeleteModel(
            name='PayByBank',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
        migrations.DeleteModel(
            name='Reserve',
        ),
    ]
