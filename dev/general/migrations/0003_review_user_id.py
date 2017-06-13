# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
