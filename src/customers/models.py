# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from core.utils import get_list_lutfiles, getLogDataRequest


LUTFILES = get_list_lutfiles()
SCALE = (
    ('1', 'simple scale png'),
    ('2', 'annotated scale')
)


def get_user_results(user, dataset, aoi, statistic):
    if statistic:
        data_polygon = DataPolygons.objects.filter(
                    user=user,
                    data_set=dataset,
                    customer_polygons=aoi,
                    statistic=statistic).order_by('id')
    else:
        data_polygon = DataPolygons.objects.filter(
                    user=user,
                    data_set=dataset,
                    customer_polygons=aoi).order_by('id')

    return data_polygon


def get_user_ts_results(user, dataset, aoi, statistic):
    if statistic:
        time_series = TimeSeriesResults.objects.filter(
                    user=user,
                    data_set=dataset,
                    customer_polygons=aoi,
                    statistic=statistic).order_by('id')
    else:
        time_series = TimeSeriesResults.objects.filter(
                    user=user,
                    data_set=dataset,
                    customer_polygons=aoi).order_by('id')

    return time_series


class LutFiles(models.Model):
    # TifPng <InpTiff> <LUTfile> [<MaxVal>] [<Legend>] [<Units>] [<ValScale>]
    
    name = models.CharField(max_length=300, blank=True, null=True)
    lut_file = models.CharField(max_length=300, blank=True, null=True,
                                choices=LUTFILES, verbose_name='LUT File')
    max_val = models.PositiveIntegerField(
                    default=100,
                    verbose_name='Maximum Value for colour scaling',)
    legend = models.CharField(
                    max_length=250,
                    blank=True, null=True,
                    choices=SCALE,
                    verbose_name='Legend',)
    units = models.CharField(
                    max_length=250,
                    blank=True, null=True,
                    verbose_name='Units',)
    val_scale = models.FloatField(
                    default=1.0,
                    verbose_name='Pixel Scale Factor for units',)
    allow_negatives = models.BooleanField(
                    default=False,
                    verbose_name='Allow negatives',)

    class Meta:
        verbose_name_plural = 'LUTFiles'

    def __unicode__(self):
        return u"{0}".format(self.name)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categorys'

    def __unicode__(self):
        return u"{0}".format(self.name)


class ShelfData(models.Model):
    category = models.ForeignKey('Category')
    attribute_name = models.CharField(
                        max_length=100,
                        blank=True,
                        null=True,
                        verbose_name='Attribute Names'
                    )
    root_filename = models.CharField(
                        max_length=100,
                        blank=True,
                        null=True,
                        verbose_name='Root Filenames'
                    )
    units = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_totals = models.BooleanField(default=True)

    lutfiles = models.ForeignKey(
                LutFiles,
                verbose_name='LUT Files',
                blank=True, null=True,
                related_name='lut_files',
                on_delete=models.CASCADE
            )

    scale = models.FloatField(
                    default=0.0,
                    verbose_name='Scale',)

    class Meta:
        verbose_name_plural = 'Shelf Data'

    def __unicode__(self):
        return u"{0}".format(self.attribute_name)


class DataSet(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    results_directory = models.CharField(max_length=150, blank=True, null=True)
    shelf_data = models.ForeignKey('ShelfData', blank=True, null=True)
    is_ts = models.BooleanField(default=False, verbose_name='Is Time Series')
    name_ts = models.CharField(max_length=300, blank=True, null=True, verbose_name='Time Series Name')

    def get_root_filename(self):
        if self.shelf_data:
            return self.shelf_data.root_filename
        return

    def get_attribute_name(self):
        if self.shelf_data:
            return self.shelf_data.attribute_name
        return

    class Meta:
        verbose_name_plural = 'DataSets'

    def __unicode__(self):
        return u"{0}".format(self.name)


class CustomerAccess(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer Name')
    data_set = models.ManyToManyField(
                    DataSet,
                    related_name='customer_access',
                    verbose_name='DataSets'
                )

    def get_data_sets(self):
        return '; '.join([p.name for p in self.data_set.all()])

    class Meta:
        verbose_name_plural = 'Customer Access'

    def __unicode__(self):
        return u"{0}".format(self.user.username)


class CustomerInfoPanel(models.Model):
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    data_set = models.ForeignKey('DataSet', blank=True, null=True)
    attribute_name = models.CharField(max_length=300, blank=True, null=True)
    statistic = models.CharField(max_length=300, blank=True, null=True)

    file_area_name = models.CharField(max_length=300, blank=True, null=True)
    tif_path = models.CharField(max_length=300, blank=True, null=True)
    png_path = models.CharField(max_length=300, blank=True, null=True)
    url_png = models.CharField(max_length=300, blank=True, null=True)

    legend_path_old = models.CharField(max_length=300, blank=True, null=True)
    legend_path = models.CharField(max_length=300, blank=True, null=True)
    url_legend = models.CharField(max_length=300, blank=True, null=True)

    is_ts = models.BooleanField(default=False, verbose_name='Is Time Series')
    order = models.PositiveIntegerField(default=0)
    is_show = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Customer Info Panel'

    def __unicode__(self):
        return u"{0}_{1}".format(self.user, self.data_set)


class CustomerPolygons(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    data_set = models.ForeignKey(
                DataSet,
                verbose_name='DataSets',
                blank=True, null=True, related_name='shapefiles',
                on_delete=models.CASCADE
            )
    kml_name = models.CharField(max_length=150, blank=True, null=True)
    kml_path = models.CharField(max_length=150, blank=True, null=True)
    kml_url = models.CharField(max_length=150, blank=True, null=True)
    text_kml = models.TextField(blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Customer Polygons'

    def __unicode__(self):
        return u"{0}".format(self.name)


class DataTerraserver(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    shapefile_link = models.CharField(max_length=250, blank=True, null=True)
    shapefile = models.CharField(max_length=250, blank=True, null=True)
    parameter = models.CharField(max_length=250, blank=True, null=True)
    transaction_id = models.CharField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = str(self.user) + '_' + str(self.shapefile)
        super(DataTerraserver, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data from Terraserver'

    def __unicode__(self):
        return u"{0}".format(self.name)


class DataPolygons(models.Model):
    data_set = models.ForeignKey(
                    DataSet,
                    verbose_name='DataSet',
                    blank=True, null=True, related_name='attributes',
                    on_delete=models.CASCADE
                )
    customer_polygons = models.ForeignKey(
                    CustomerPolygons,
                    verbose_name='Customer Polygons',
                    blank=True, null=True, related_name='attributes_shapefile',
                    on_delete=models.CASCADE
                )
    user = models.ForeignKey(User, verbose_name='Polygons User',
                blank=True, null=True, related_name='shapefiles_user',
                on_delete=models.CASCADE
            )
    attribute = models.CharField(max_length=250, blank=True, null=True)
    statistic = models.CharField(max_length=250, blank=True, null=True)
    value = models.CharField(max_length=250, blank=True, null=True)
    units = models.CharField(max_length=250, blank=True, null=True)
    total = models.CharField(max_length=250, blank=True, null=True)
    total_area = models.CharField(max_length=250, blank=True, null=True)
    
    def __unicode__(self):
        return u"data_{0}".format(self.customer_polygons)


class AttributesReport(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                blank=True, null=True, related_name='users_attributes_reports',
                on_delete=models.CASCADE
            )
    data_set = models.ForeignKey(
                    DataSet,
                    verbose_name='DataSet',
                    blank=True, null=True, related_name='attributes_datasets',
                    on_delete=models.CASCADE
                )
    shelfdata = models.ForeignKey(
                    ShelfData,
                    verbose_name='ShelfData',
                    blank=True, null=True, related_name='attributes_shelfdata',
                    on_delete=models.CASCADE
                )
    statistic = models.CharField(max_length=250, blank=True, null=True)
    attribute = models.CharField(max_length=300, blank=True, null=True)


# Max, Min, Mean,LQ (Lower Quartile), UQ (Upper Quartile)
STAT_SUB_DIRECTORIES = (
    ('1', 'Max'),
    ('2', 'Min'),
    ('3', 'Mean'),
    ('4', 'Lower Quartile'),
    ('5', 'Upper Quartile'),
)


class TimeSeriesResults(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, verbose_name='User',
                related_name='time_series_user',
                on_delete=models.CASCADE
            )
    data_set = models.ForeignKey(
                    DataSet,
                    verbose_name='DataSet',
                    related_name='timeseries',
                    on_delete=models.CASCADE
                )
    customer_polygons = models.ForeignKey(
                    CustomerPolygons,
                    verbose_name='Customer Polygons',
                    related_name='timeseries_attributes',
                    on_delete=models.CASCADE
                )
    result_year = models.CharField(
                    max_length=4,
                    verbose_name='Result Year',)
    stat_code = models.CharField(
                    max_length=25,
                    # choices=STAT_SUB_DIRECTORIES,
                    verbose_name='Status Sub Directory',)
    result_date = models.DateField(verbose_name='Result Date')
    value_of_time_series = models.CharField(
                            max_length=250,
                            blank=True, null=True,
                            verbose_name='Value',)
    attribute = models.CharField(
                            max_length=250,
                            blank=True, null=True,
                            verbose_name='Attribute',)

    def __unicode__(self):
        return u"{0}".format(self.name)


class Reports(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, verbose_name='User',
                related_name='report_user',
                on_delete=models.CASCADE
            )
    dataset = models.ForeignKey(
                    DataSet,
                    verbose_name='DataSet',
                    related_name='report_dataset',
                    on_delete=models.CASCADE
                )
    shelfdata = models.ForeignKey(
                    ShelfData,
                    verbose_name='ShelfData',
                    related_name='report_shelfdata',
                    on_delete=models.CASCADE
                )

    def __unicode__(self):
        return u"{0}".format(self.name)


class Log(models.Model):
    """ log system """

    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='log_user',
        on_delete=models.CASCADE
    )
    mode = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='Mode'
    )
    dataset = models.ForeignKey(
        DataSet,
        verbose_name='DataSet',
        related_name='log_dataset',
        blank=True, null=True,
        on_delete=models.CASCADE
    )
    action = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='Action'
    )
    shapefile = models.ForeignKey(
        CustomerPolygons,
        verbose_name='Shapefile',
        related_name='results',
        blank=True, null=True,
        on_delete=models.CASCADE
    )
    ip = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='IP'
    )
    os_user = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='OS'
    )
    browser = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='Browser'
    )
    command = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name='Command'
    )
    message = models.TextField(null=False, default='')
    status_message = models.TextField(null=False, default='')
    at = models.DateTimeField(auto_now_add=True)

    def get_results(self, statistic=None):
        return get_user_results(self.user, self.dataset, self.shapefile, statistic)

    def get_ts_results(self, statistic=None):
        return get_user_ts_results(self.user, self.dataset, self.shapefile, statistic)

    def __unicode__(self):
        return u"log {0}: {1} | {2} | {3}".format(self.at, self.user, self.mode, self.action)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if 'admin' in request.META.get('HTTP_REFERER'):
        return

    if 'register' in request.META.get('HTTP_REFERER'):
        action = 'register'

    try:
        cip = CustomerInfoPanel.objects.get(user=user, is_show=True)
        dataset = cip.data_set
    except CustomerInfoPanel.DoesNotExist:
        dataset = None

    status_message = '{}'.format('success')
    message = getLogDataRequest(request)
    Log.objects.create(user=user, mode='ui', dataset=dataset,
        action='login', message=message, status_message=status_message,
        ip=request.META.get('REMOTE_ADDR'))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    try:
        cip = CustomerInfoPanel.objects.get(user=user, is_show=True)
        dataset = cip.data_set
    except CustomerInfoPanel.DoesNotExist:
        dataset = None

    status_message = '{}'.format('success')
    message = getLogDataRequest(request)
    Log.objects.create(user=user, mode='ui', dataset=dataset,
        action='logout', message=message, status_message=status_message,
        ip=request.META.get('REMOTE_ADDR'))


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     Log.objects.create(user=instance, mode='ui', action='register')


# @receiver(user_login_failed)
# def user_login_failed_callback(sender, credentials, **kwargs):
#     # message = getLogDataRequest(request)
#     Log.objects.create(mode='ui', action='login failed', message=credentials.get('username', None))


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     Log.objects.create(user=sender, mode='api', action='login', message=sender)

