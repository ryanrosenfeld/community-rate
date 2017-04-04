# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_review_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_added',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 4, 4, 3, 16, 13, 877738, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
