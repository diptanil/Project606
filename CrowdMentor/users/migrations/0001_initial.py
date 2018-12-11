# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 19:29
from __future__ import unicode_literals

from users import UserRoles
from decimal import Decimal
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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(null=True)),
                ('role', models.CharField(choices=[(UserRoles.UserRoles(b'admin'), b'admin'),
                                                   (UserRoles.UserRoles(b'auditor'), b'auditor'),
                                                   (UserRoles.UserRoles(b'mentor'), b'mentor'),
                                                   (UserRoles.UserRoles(b'task_updater'), b'task_updater'),
                                                   (UserRoles.UserRoles(b'worker'), b'worker')],
                                          default=UserRoles.UserRoles(b'worker'), max_length=15)),
                ('performance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5)),
                ('salary', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('bonus', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('fine', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('total_salary', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('audit_prob_user', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mentor', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
