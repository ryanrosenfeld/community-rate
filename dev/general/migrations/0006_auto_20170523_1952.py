# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0005_delete_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='about_me',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='fav_quote',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='fb_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
