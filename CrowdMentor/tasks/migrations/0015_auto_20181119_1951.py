# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-19 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20181028_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskuserjunction',
            name='answer',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
