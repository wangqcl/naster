# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-06-29 17:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20200629_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compinfo',
            old_name='Leak_scan',
            new_name='leak_scan',
        ),
    ]
