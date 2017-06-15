# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-06 04:03
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_dict', models.TextField(
                    verbose_name='It will save all entries of Log model Instance. If user deleted then that data will show to user information in admin')),
                ('log', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='admin.LogEntry', verbose_name='Logs')),
            ],
            options={
                'verbose_name_plural': 'Log Entries',
                'verbose_name': 'Log Entry',
            },
        ),
    ]
