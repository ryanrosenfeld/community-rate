# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0009_siteuser_has_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='timezone',
            field=models.CharField(default='US/Eastern', max_length=100),
        ),
    ]
