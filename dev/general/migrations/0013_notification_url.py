# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-25 03:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_siteuser_reset_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]