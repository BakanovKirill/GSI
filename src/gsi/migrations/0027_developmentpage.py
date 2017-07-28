# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0026_auto_20160909_0806'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevelopmentPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=300)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
