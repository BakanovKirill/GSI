# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0027_auto_20170510_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapolygons',
            name='user',
            field=models.ForeignKey(related_name='user_data_polygons', verbose_name=b'User Polygons', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
