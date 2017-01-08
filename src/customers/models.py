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
    attribute_name = models.CharField(max_length=100, blank=True, null=True)
    root_filename = models.CharField(max_length=100, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Shelf Data'

    def __unicode__(self):
        return u"{0}".format(self.attribute_name)


# class DataSet(models.Model):
#     pass
    # name = models.CharField(max_length=50)
    # description = models.CharField(max_length=150)
    # results_directory = models.CharField(max_length=250)
    #
    # class Meta:
    #     verbose_name_plural = 'DataSets'
