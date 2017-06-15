# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User


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

    class Meta:
        verbose_name_plural = 'Shelf Data'

    def __unicode__(self):
        return u"{0}".format(self.attribute_name)


LUTFILES = (
    ('grey', 'Grey'),
    ('red', 'Red'),
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'), )


class DataSet(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    results_directory = models.CharField(max_length=150, blank=True, null=True)
    shelf_data = models.ForeignKey('ShelfData', blank=True, null=True)
    
    lutfile = models.CharField(max_length=50, choices=LUTFILES, default='running')
    
    # lut_file = models.CharField(
    #                 max_length=250,
    #                 blank=True, null=True,
    #                 verbose_name='LUT file',)
    max_val = models.PositiveIntegerField(
                    default=100,
                    blank=True, null=True,
                    verbose_name='Maximum Value for colour scaling',)
    legend = models.CharField(
                    max_length=250,
                    blank=True, null=True,
                    verbose_name='Legend',)
                    
                    
    # set_color_png = models.ForeignKey(
    #             SetColorPng,
    #             verbose_name='SetColorPng',
    #             blank=True, null=True, related_name='set_color_png',
    #             on_delete=models.CASCADE
    #         )
    

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
    attribute_name = models.CharField(max_length=150, blank=True, null=True)
    statisctic = models.CharField(max_length=150, blank=True, null=True)

    file_area_name = models.CharField(max_length=150, blank=True, null=True)
    tif_path = models.CharField(max_length=150, blank=True, null=True)
    png_path = models.CharField(max_length=150, blank=True, null=True)
    url_png = models.CharField(max_length=150, blank=True, null=True)
    
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
    

    class Meta:
        verbose_name_plural = 'Customer Polygons'

    def __unicode__(self):
        return u"{0}_{1}".format(self.user, self.name)
        
        
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
    statisctic = models.CharField(max_length=250, blank=True, null=True)
    value = models.CharField(max_length=250, blank=True, null=True)
    units = models.CharField(max_length=250, blank=True, null=True)
    total = models.CharField(max_length=250, blank=True, null=True)
    total_area = models.CharField(max_length=250, blank=True, null=True)
    
    
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
    statisctic = models.CharField(max_length=250, blank=True, null=True)


class CountFiles(models.Model):
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    count = models.PositiveIntegerField(default=0)
    
    
# class LutFile(models.Model):
#     name = models.CharField(max_length=300, blank=True, null=True)
#     data_color = models.TextField()
    
    
# class SetColorPng(models.Model):
#     name =  = models.CharField(max_length=250, blank=True, null=True)
#     lut_file = models.CharField(max_length=250, blank=True, null=True)
#     max_val = models.CharField(max_length=250, blank=True, null=True)
#     legend = models.CharField(max_length=250, blank=True, null=True)
#
#     def __unicode__(self):
#         return u"{0}".format(self.name)
    
