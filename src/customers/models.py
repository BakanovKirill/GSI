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
    attribute_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Attribute Name')
    root_filename = models.CharField(max_length=100, blank=True, null=True, verbose_name='Root Filename')
    units = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Shelf Data'

    def __unicode__(self):
        return u"{0}".format(self.attribute_name)


class DataSet(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    results_directory = models.CharField(max_length=150, blank=True, null=True)
    shelf_data = models.ForeignKey('ShelfData', blank=True, null=True)

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
    data_set = models.ManyToManyField(DataSet, related_name='customer_access', verbose_name='DataSets')

    def get_data_sets(self):
        return '; '.join([p.name for p in self.data_set.all()])

    class Meta:
        verbose_name_plural = 'Customer Access'

    def __unicode__(self):
        return u"{0}".format(self.user.username)


# class SelectedArea(models.Model):
#     user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
#     project = models.CharField(max_length=150, blank=True, null=True)
#     attribute_name = models.CharField(max_length=150, blank=True, null=True)
#     statistics = models.CharField(max_length=150, blank=True, null=True)
#     polygon = models.CharField(max_length=150, blank=True, null=True)
#
#     class Meta:
#         verbose_name_plural = 'Selected Area'
#
#     def __unicode__(self):
#         return u"{0}_{1}_{2}".format(self.statistics)
