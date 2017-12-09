# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0073_lutfiles_allow_negatives'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('dataset', models.ForeignKey(related_name='report_dataset', verbose_name=b'DataSet', to='customers.DataSet')),
                ('shelfdata', models.ForeignKey(related_name='report_shelfdata', verbose_name=b'ShelfData', to='customers.ShelfData')),
                ('user', models.ForeignKey(related_name='report_user', verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='lutfiles',
            name='lut_file',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'LUT File', choices=[(b'select', b'select'), (b'red-blue.lut', b'red-blue.lut'), (b'16colours.txt', b'16colours.txt'), (b'10colours.txt', b'10colours.txt'), (b'green.txt', b'green.txt'), (b'MMdiffCols.txt', b'MMdiffCols.txt'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'CompositeCols.txt', b'CompositeCols.txt'), (b'red.lut', b'red.lut'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt'), (b'MM16colors.txt', b'MM16colors.txt'), (b'RedHot.lut', b'RedHot.lut'), (b'TEST1.txt', b'TEST1.txt'), (b'blue.txt', b'blue.txt'), (b'Low-HighBreakpoints.txt', b'Low-HighBreakpoints.txt'), (b'Viridis.txt', b'Viridis.txt'), (b'red.txt', b'red.txt'), (b'treed.txt', b'treed.txt'), (b'16colours.txt.old', b'16colours.txt.old'), (b'2016_L8_RGB.lut', b'2016_L8_RGB.lut'), (b'2006_L7_RGB.lut', b'2006_L7_RGB.lut')]),
        ),
    ]
