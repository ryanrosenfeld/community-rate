# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-15 17:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0010_siteuser_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notification_class',
        ),
    ]