# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0028_datapolygons_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpolygons',
            name='data_set',
            field=models.ForeignKey(related_name='shapefiles', verbose_name=b'Shapefiles', blank=True, to='customers.DataSet', null=True),
        ),
        migrations.AlterField(
            model_name='datapolygons',
            name='customer_polygons',
            field=models.ForeignKey(related_name='attributes_shapefile', verbose_name=b'Shapefiles attributes', blank=True, to='customers.CustomerPolygons', null=True),
        ),
        migrations.AlterField(
            model_name='datapolygons',
            name='data_set',
            field=models.ForeignKey(related_name='attributes', verbose_name=b'Attributes', blank=True, to='customers.DataSet', null=True),
        ),
        migrations.AlterField(
            model_name='datapolygons',
            name='user',
            field=models.ForeignKey(related_name='shapefiles_user', verbose_name=b'Polygons User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
