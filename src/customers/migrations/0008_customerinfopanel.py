# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0007_customeraccess'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfoPanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_name', models.CharField(max_length=150, null=True, blank=True)),
                ('statisctic', models.CharField(max_length=150, null=True, blank=True)),
                ('polygon', models.CharField(max_length=150, null=True, blank=True)),
                ('tif_path', models.CharField(max_length=150, null=True, blank=True)),
                ('png_path', models.CharField(max_length=150, null=True, blank=True)),
                ('data_set', models.ForeignKey(blank=True, to='customers.DataSet', null=True)),
                ('user', models.ForeignKey(verbose_name=b'User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Customer Info Panel',
            },
        ),
    ]
