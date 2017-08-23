# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0059_auto_20170822_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSeriesResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('result_year', models.CharField(max_length=4)),
                ('stat_code', models.CharField(max_length=25, verbose_name=b'Status Sub Directory', choices=[(b'1', b'Max'), (b'2', b'Min'), (b'3', b'Mean'), (b'4', b'Lower Quartile'), (b'5', b'Upper Quartile')])),
                ('result_date', models.DateField()),
                ('value_of_time_series', models.CharField(max_length=250)),
                ('customer_polygons', models.ForeignKey(related_name='ts_attributes', verbose_name=b'Time Series Customer Polygons', to='customers.CustomerPolygons')),
                ('data_set', models.ForeignKey(related_name='ts_datasets', verbose_name=b'Time Series DataSet', to='customers.DataSet')),
                ('user', models.ForeignKey(related_name='time_series_user', verbose_name=b'Time Series User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
