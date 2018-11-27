# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-27 03:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broadcast_type', models.CharField(blank=True, max_length=10, null=True)),
                ('broadcast_message', models.CharField(default='Enter a single line summary', max_length=500)),
                ('group_role', models.CharField(blank=True, max_length=10, null=True)),
                ('claim', models.BooleanField(default=False)),
                ('claim_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
