# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0006_auto_20170110_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_set', models.ManyToManyField(related_name='customer_access', verbose_name=b'DataSets', to='customers.DataSet')),
                ('user', models.ForeignKey(verbose_name=b'Customer Name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Access',
            },
        ),
    ]
