# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0011_remove_notification_notification_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='reset_key',
            field=models.TextField(default='1'),
        ),
    ]