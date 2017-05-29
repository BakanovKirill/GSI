# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0035_datapolygons_statisctic'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributesReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=250, null=True, blank=True)),
                ('data_set', models.ForeignKey(related_name='attributes_datasets', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True)),
                ('user', models.ForeignKey(related_name='users_attributes_reports', verbose_name=b'User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
