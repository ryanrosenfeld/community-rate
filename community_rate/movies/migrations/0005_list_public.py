# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_list_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
