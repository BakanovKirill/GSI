# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0019_customerpolygons_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPolygons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('value', models.CharField(max_length=250, null=True, blank=True)),
                ('customer_polygons', models.ForeignKey(verbose_name=b'Customer Polygons', blank=True, to='customers.CustomerPolygons', null=True)),
            ],
        ),
    ]
