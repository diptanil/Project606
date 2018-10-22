# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 20:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mentor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[(b'admin', b'admin'), (b'auditor', b'auditor'), (b'mentor', b'mentor'), (b'task_updater', b'task_updater'), (b'worker', b'worker')], default=b'worker', max_length=15),
        ),
    ]