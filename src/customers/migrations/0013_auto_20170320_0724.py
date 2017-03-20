# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0012_customerinfopanel_polygon'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPolygons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
                ('kml_name', models.CharField(max_length=150, null=True, blank=True)),
                ('user', models.ForeignKey(verbose_name=b'User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Customer Polygons',
            },
        ),
        migrations.RemoveField(
            model_name='customerinfopanel',
            name='polygon',
        ),
    ]
