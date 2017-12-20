# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0074_auto_20171208_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mode', models.CharField(max_length=250, null=True, verbose_name=b'Mode', blank=True)),
                ('action', models.CharField(max_length=250, null=True, verbose_name=b'Action', blank=True)),
                ('at', models.DateTimeField(auto_now_add=True)),
                ('customer_polygons', models.ForeignKey(related_name='results', verbose_name=b'Customer Polygon', blank=True, to='customers.CustomerPolygons', null=True)),
                ('dataset', models.ForeignKey(related_name='log_dataset', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True)),
                ('user', models.ForeignKey(related_name='log_user', verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
