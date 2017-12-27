# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0077_log_status_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='customer_polygons',
            new_name='shapefile',
        ),
    ]
