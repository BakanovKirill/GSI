# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import gsi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CardSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('environment_override', models.TextField(null=True, blank=True)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HomeVariables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SAT_TIF_DIR_ROOT', models.CharField(help_text='SAT_TIF_DIR_ROOT', max_length=300, verbose_name='Satelite Data Top Level')),
                ('RF_DIR_ROOT', models.CharField(help_text='RF_DIR_ROOT', max_length=300, verbose_name='Top directory of Random Forest Files')),
                ('USER_DATA_DIR_ROOT', models.CharField(help_text='USER_DATA_DIR_ROOT', max_length=300, verbose_name='Top Level for user data directory')),
                ('MODIS_DIR_ROOT', models.CharField(help_text='MODIS_DIR_ROOT', max_length=300, verbose_name='Top Level for raw Modis data')),
                ('RF_AUXDATA_DIR', models.CharField(help_text='RF_AUXDATA_DIR', max_length=300, verbose_name='Top Level for Auxilliary data(SOIL, DEM etc.)')),
                ('SAT_DIF_DIR_ROOT', models.CharField(help_text='SAT_DIF_DIR_ROOT', max_length=300, verbose_name='Top Level for Satelite TF files')),
            ],
            options={
                'verbose_name': 'Home variables',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('log_file_path', models.CharField(max_length=300, null=True, blank=True)),
                ('log_file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrderedCardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('card_item', models.ForeignKey(related_name='ordered_cards', to='cards.CardItem')),
                ('sequence', models.ForeignKey(to='gsi.CardSequence')),
            ],
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='This will be a short display of the value, i.e. 1KM, 250M', max_length=50)),
                ('value', models.CharField(help_text='Value in meters, e.g 1000 for 1KM display name', max_length=20)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'created', max_length=100, choices=[(b'created', b'Created'), (b'pending', b'Pending'), (b'running', b'Running'), (b'success', b'Success'), (b'fail', b'Fail')])),
                ('run_date', models.DateTimeField(auto_now_add=True)),
                ('log', models.ForeignKey(blank=True, to='gsi.Log', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RunBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('purpose', models.TextField(null=True, blank=True)),
                ('directory_path', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('card_sequence', models.ForeignKey(to='gsi.CardSequence')),
                ('resolution', models.ForeignKey(to='gsi.Resolution')),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RunStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'pending', max_length=100, choices=[(b'created', b'Created'), (b'pending', b'Pending'), (b'running', b'Running'), (b'success', b'Success'), (b'fail', b'Fail')])),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('card_item', models.ForeignKey(to='cards.CardItem')),
                ('parent_run', models.ForeignKey(to='gsi.Run')),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=6)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TileType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VariablesGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('environment_variables', models.TextField()),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=4)),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='YearGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('years', models.ManyToManyField(related_name='year_groups', to='gsi.Year')),
            ],
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.AddField(
            model_name='run',
            name='run_base',
            field=models.ForeignKey(to='gsi.RunBase'),
        ),
        migrations.AddField(
            model_name='run',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='cardsequence',
            name='cards',
            field=models.ManyToManyField(related_name='card_sequences', through='gsi.OrderedCardItem', to='cards.CardItem'),
        ),
        migrations.AddField(
            model_name='cardsequence',
            name='environment_base',
            field=models.ForeignKey(blank=True, to='gsi.VariablesGroup', null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='tiles',
            field=models.ManyToManyField(related_name='areas', to='gsi.Tile'),
        ),
    ]
