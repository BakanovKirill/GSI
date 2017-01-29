# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0010_customerinfopanel_url_png'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerinfopanel',
            name='polygon',
        ),
    ]
