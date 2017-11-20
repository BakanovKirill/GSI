# -*- coding: utf-8 -*-
"""Views for the customers app."""
import time
import os
import os.path, time
import subprocess
from PIL import Image
from subprocess import check_call, Popen, PIPE
from osgeo import osr, gdal, ogr
import simplekml
from simplekml import Kml, ColorMode, AltitudeMode, Style
import pickle
from datetime import datetime, date, timedelta
import json
import csv
from pykml import parser
from pykml.parser import Schema
from lxml import html
import numpy as np
import requests
from random import randint
import re

# import pykml
# from pykml import parser
# from pykml.parser import Schema
# import urllib2

# import Image, ImageDraw
# from osgeo import gdal
# import gdal

from django.shortcuts import render
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import redirect

from customers.models import (Category, ShelfData, DataSet, CustomerAccess,
                                CustomerInfoPanel, CustomerPolygons, DataPolygons,
                                AttributesReport, LutFiles, TimeSeriesResults)
from customers.customers_forms import (CategoryForm, ShelfDataForm, DataSetForm,
                                        CustomerAccessForm, CustomerPolygonsForm,
                                        LutFilesForm)
from customers.customers_update_create import (category_update_create, shelf_data_update_create,
                                                data_set_update_create, customer_access_update_create,
                                                lutfile_update_create)
from core.get_post import get_post
from core.paginations import paginations
from core.utils import handle_uploaded_file, get_files_dirs, get_list_lutfiles
from gsi.settings import (BASE_DIR, GOOGLE_MAP_ZOOM, MEDIA_ROOT,
                        TMP_PATH, DAFAULT_LAT, DAFAULT_LON, PNG_DIRECTORY, PNG_PATH,
                        PROJECTS_PATH, KML_DIRECTORY, KML_PATH, ATTRIBUTES_NAME, FTP_PATH,
                        LUT_DIRECTORY, SCRIPT_TIFPNG, SCRIPT_GETPOLYINFO, LEGENDS_DIRECTORY,
                        LEGENDS_PATH, SCRIPT_MAXSIZE, ATTRIBUTE_CONFIG, COLOR_HEX_NAME, COLOR_HEX)
from gsi.gsi_forms import UploadFileForm


SUB_DIRECTORIES = {
    'mean_ConditionalMax': 'Max',
    'mean_ConditionalMean': 'Mean',
    'mean_ConditionalMedian': 'Median',
    'mean_ConditionalMin': 'Min',
    'mean_LowerQuartile': 'LQ',
    'mean_Quantile': 'UQ',
}

SUB_DIRECTORIES_REVERCE = {
    'Max': 'mean_ConditionalMax',
    'Mean': 'mean_ConditionalMean',
    'Median': 'mean_ConditionalMedian',
    'Min': 'mean_ConditionalMin',
    'LQ': 'mean_LowerQuartile',
    'UQ': 'mean_Quantile',
}

# categorys list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/categorys_list.html')
def categorys(request):
    """**View all categories for the Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The categorys for the Shelf Data'
    url_name = 'categorys'
    but_name = 'info_panel'

    categorys = Category.objects.all().order_by('name')
    category_name = ''

    # Sorted by
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            categorys = categorys.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                categorys = categorys.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Category, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Category, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('category_select'):
            for category_id in request.POST.getlist('category_select'):
                cur_category = get_object_or_404(Category, pk=category_id)
                category_name += '"' + cur_category.name + '", '
                cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'),
                (u'Categorys: {0} deleted.'.format(category_name))))
        elif request.POST.get('delete_button'):
            cur_category = get_object_or_404(Category, pk=request.POST.get('delete_button'))
            category_name += '"' + cur_category.name + '", '
            cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'), (u'Categorys: {0} deleted.'.format(category_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('categorys_list'), (u"To delete, select Category or more Categorys.")))

    # paginations
    model_name = paginations(request, categorys)

    data = {
        'title': title,
        'categorys': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category add
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_add(request):
    """**View for the "Category Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Category Add'
    url_form = 'category_add'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CategoryForm, 'Category', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        # 'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_edit(request, category_id):
    """**View for the "Category "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *category_id:* The Category object ID
    """

    category = get_object_or_404(Category, pk=category_id)
    title = 'Category Edit "%s"' % (category.name)
    url_form = 'category_edit'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            CategoryForm,
            'Category',
            reverse_url,
            func,
            item_id=category_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm(instance=category)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': category_id,
    }

    return data


# shelf data list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/shelf_data_list.html')
def shelf_data(request):
    """**View all Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The Shelf Data'
    url_name = 'shelf_data'
    but_name = 'info_panel'

    shelf_data = ShelfData.objects.all().order_by('attribute_name')
    shelf_data_name = ''

    # Sorted
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('category', 'attribute_name', 'root_filename', 'units', 'scale',):
            shelf_data = shelf_data.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                shelf_data = shelf_data.reverse()

        if order_by in ('lutfiles',):
            shelf_data = shelf_data.order_by('lutfiles__name')

            if request.GET.get('reverse', '') == '1':
                shelf_data = shelf_data.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(ShelfData, pk=int(r))
                data += '"' + str(cur_run) + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(ShelfData, pk=int(run_id))
            data = '<b>"' + str(cur_run) + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('shelf_data_select'):
            for shelf_data_id in request.POST.getlist('shelf_data_select'):
                cur_shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
                shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
                cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data'),
                (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        elif request.POST.get('delete_button'):
            cur_shelf_data = get_object_or_404(ShelfData, pk=request.POST.get('delete_button'))
            shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
            cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data'), (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('shelf_data'), (u"To delete, select Shelf Data or more Shelf Data.")))

    # paginations
    model_name = paginations(request, shelf_data)

    data = {
        'title': title,
        'shelf_data': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_add(request):
    """**View for the "ShelfData Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Shelf Data Add'
    url_form = 'shelf_data_add'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'
    available_tiles = ShelfData.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, ShelfDataForm, 'Shelf Data', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_edit(request, shelf_data_id):
    """**View for the "ShelfData "<attribute_name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *shelf_data_id:* The ShelfData object ID
    """

    shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
    title = 'ShelfData Edit "%s"' % (shelf_data.attribute_name)
    url_form = 'shelf_data_edit'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            ShelfDataForm,
            'Shelf Data',
            reverse_url,
            func,
            item_id=shelf_data_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm(instance=shelf_data)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': shelf_data_id,
    }

    return data


# data sets list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/dataset_list.html')
def data_sets(request):
    """**View all the DataSets.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'DataSets Definition'
    url_name = 'data_sets'
    but_name = 'info_panel'

    data_sets = DataSet.objects.all().order_by('name')
    data_set_name = ''

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'description', 'results_directory', 'shelf_data__attribute_name', 'shelf_data__root_filename'):
            data_sets = data_sets.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                data_sets = data_sets.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(DataSet, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(DataSet, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('dataset_select'):
            for data_set_id in request.POST.getlist('dataset_select'):
                cur_data_set = get_object_or_404(DataSet, pk=data_set_id)
                data_set_name += '"' + cur_data_set.name + '", '
                cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'),
                (u'DataSets: {0} deleted.'.format(data_set_name))))
        elif request.POST.get('delete_button'):
            cur_data_set = get_object_or_404(DataSet, pk=request.POST.get('delete_button'))
            data_set_name += '"' + cur_data_set.name + '", '
            cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'), (u'DataSets: {0} deleted.'.format(data_set_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('data_sets'), (u"To delete, select DataSet or more DataSets.")))

    # paginations
    model_name = paginations(request, data_sets)

    data = {
        'title': title,
        'data_sets': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_add(request):
    """**View for the "DataSet Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'DataSet Add'
    url_form = 'data_set_add'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)


    # Handling POST request
    if request.method == "POST":
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    try:
                        results_directory = PROJECTS_PATH + form.cleaned_data['results_directory']
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_add'),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'url_name': url_name,
        'but_name': but_name,
        'dirs_list': dirs_list,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_edit(request, data_set_id):
    """**View for the "DataSets "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *data_set_id:* The ShelfData object ID
    """

    data_set = get_object_or_404(DataSet, pk=data_set_id)
    title = 'DataSet Edit "%s"' % (data_set.name)
    url_form = 'data_set_edit'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Get the results_directorys list
    try:
        results_directory = PROJECTS_PATH + data_set.results_directory
        root, dirs, files = os.walk(results_directory).next()

        for sd in shelf_data:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)
    except Exception:
        pass

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        # Update the results_directorys list
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)
            dirs_list = []

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    results_directory = PROJECTS_PATH + form.cleaned_data['results_directory']

                    try:
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func, item_id=data_set_id)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm(instance=data_set)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': data_set_id,
        'data_set': data_set,
        'dirs_list': dirs_list,
    }

    return data


# customers access list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/customer_access_list.html')
def customer_access(request):
    """**View the Customer Access.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'Customer Access'
    url_name = 'customer_access'
    but_name = 'info_panel'

    customers_access = CustomerAccess.objects.all().order_by('user__username')
    customer_access_name = ''

    # Sorted by customer name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('user', ):
            customers_access = customers_access.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                customers_access = customers_access.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(CustomerAccess, pk=int(r))
                data += '"{0}", '.format(cur_run)

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(CustomerAccess, pk=int(run_id))
            data = '<b>"{0}"</b>'.format(cur_run)
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('customer_access_select'):
            for customer_access_id in request.POST.getlist('customer_access_select'):
                cur_customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
                customer_access_name += '"{0}" '.format(cur_customer_access)
                cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'),
                (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        elif request.POST.get('delete_button'):
            cur_customer_access = get_object_or_404(CustomerAccess, pk=request.POST.get('delete_button'))
            customer_access_name += '"{0}", '.format(cur_customer_access)
            cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'), (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('customer_access'), (u"To delete, select Customer Access or more Customers Access.")))

    # paginations
    model_name = paginations(request, customers_access)

    data = {
        'title': title,
        'customers_access': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access add
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_add(request):
    """**View for the "Customer Access Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Customer Access Add'
    url_form = 'customer_access_add'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    available_data_set = DataSet.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CustomerAccessForm, 'Customer Access', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_data_set': available_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_edit(request, customer_access_id):
    """**View for the "Customer Access "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *customer_access_id:* The CustomerAccess object ID
    """

    customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
    title = 'Customer Access Edit "%s"' % (customer_access)
    url_form = 'customer_access_edit'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    chosen_data_set = customer_access.data_set.all()
    available_data_set = DataSet.objects.exclude(id__in=customer_access.data_set.values_list('id', flat=True))

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request, CustomerAccessForm, 'Customer Access', reverse_url, func, item_id=customer_access_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm(instance=customer_access)

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'item_id': customer_access_id,
        'available_data_set': available_data_set,
        'chosen_data_set': chosen_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# LUT Files list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/lutfiles_list.html')
def lutfiles(request):
    """**View the LUT Files.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'LUT Files'
    url_name = 'lutfiles'
    but_name = 'info_panel'

    lutfiles = LutFiles.objects.all().order_by('name')
    lutfiles_name = ''

    # Sorted by customer name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'filename', 'max_val', 'lut_file'):
            lutfiles = lutfiles.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                lutfiles = lutfiles.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_lutfile = get_object_or_404(LutFiles, pk=int(r))
                data += '"{0}", '.format(cur_lutfile)

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_lutfile = get_object_or_404(LutFiles, pk=int(run_id))
            data = '<b>"{0}"</b>'.format(cur_lutfile)
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('lutfiles_select'):
            for lutfile_id in request.POST.getlist('lutfiles_select'):
                cur_lutfile = get_object_or_404(LutFiles, pk=lutfile_id)
                lutfiles_name += '"{0}", '.format(cur_lutfile)
                cur_lutfile.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('lutfiles'),
                (u'LUT Files: {0} deleted.'.format(lutfiles_name))))
        elif request.POST.get('delete_button'):
            cur_lutfile = get_object_or_404(LutFiles, pk=request.POST.get('delete_button'))
            lutfiles_name += '"{0}", '.format(cur_lutfile)
            cur_lutfile.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('lutfiles'), (u'LUT File: {0} deleted.'.format(lutfiles_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('lutfiles'), (u"To delete, select LUT File or more LUT Files.")))

    # paginations
    model_name = paginations(request, lutfiles)

    data = {
        'title': title,
        'lutfiles': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access add
@login_required
@render_to('gsi/static_data_item_edit.html')
def lutfile_add(request):
    """**View for a new LUT File.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'LUT File Add'
    url_form = 'lutfile_add'
    template_name = 'customers/_lutfile_form.html'
    reverse_url = {
        'save_button': 'lutfiles',
        'save_and_another': 'lutfile_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'lutfiles'
    }
    func = lutfile_update_create
    form = None
    url_name = 'lutfiles'
    but_name = 'info_panel'
    list_lutfiles = get_list_lutfiles()

    print '!!!!!!!!!!! LIST LUT FILES =========================== ', list_lutfiles

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, LutFilesForm, 'LUT File', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = LutFilesForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# lutfile edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def lutfile_edit(request, lutfile_id):
    """**View for the "Category "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *lutfile_id:* The Category object ID
    """

    lutfile = get_object_or_404(LutFiles, pk=lutfile_id)
    title = 'LUT File Edit "%s"' % (lutfile.name)
    url_form = 'lutfile_edit'
    template_name = 'customers/_lutfile_form.html'
    reverse_url = {
        'save_button': 'lutfiles',
        'save_and_another': 'lutfile_add',
        'save_and_continue': 'lutfile_edit',
        'cancel_button': 'lutfiles'
    }
    func = lutfile_update_create
    form = None
    url_name = 'lutfiles'
    but_name = 'info_panel'
    list_lutfiles = get_list_lutfiles()

    # get AJAX POST for KML files
    if request.is_ajax() and request.method == "GET":
        data_get_ajax = request.GET
        data = ''

        if 'update' in data_get_ajax:
            customer = request.user
            cip = CustomerInfoPanel.objects.filter(user=customer)

            for cp in cip:
                try:
                    os.remove(cp.png_path)
                except Exception:
                    pass

            # cip.delete()

        return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            LutFilesForm,
            'LUT File',
            reverse_url,
            func,
            item_id=lutfile_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = LutFilesForm(instance=lutfile)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': lutfile_id,
    }

    return data


def remove_files(file_path):
    # Get the png file for the delete
    
    try:
        os.remove(file_path)
    except Exception, e:
        print '!!!!!!!!!!! Exception remove file png ========================= ', e
        pass


def check_current_dataset(request, data_post):
    is_delete = False
    data_set_id = data_post.get('datasets_id', '')
    request.session['select_data_set'] = data_set_id
    data_set = DataSet.objects.get(pk=data_set_id)

    # print 'data_set_id ==================================', request.session['select_data_set']

    if not CustomerInfoPanel.objects.filter(user=request.user, data_set=data_set).exists():
        info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
        is_delete = True

    return is_delete


def check_date_files(file_tif, file_png):
    try:
        f_tif = os.path.getmtime(file_tif)
        f_png = os.path.getmtime(file_png)

        if f_tif > f_png:
            return True
    except Exception, e:
        print '---> Exception check_date_files ========================= ', e
        return True

    return False


ATTRIBUTE_NAMES = [
    'mean_ConditionalMax',
    'mean_ConditionalMean',
    'mean_ConditionalMedian',
    'mean_ConditionalMin',
    'mean_LowerQuartile',
    'mean_Quantile'
]


def checkKmlFile(filename):
    kml_filename = filename + '.kml'
    file_path = os.path.join(KML_PATH, kml_filename)

    if os.path.exists(file_path):
        for n in xrange(1000000):
            fn = filename + '_' + str(n)
            kml_filename = fn + '.kml'
            file_path = os.path.join(KML_PATH, kml_filename)

            if not os.path.exists(file_path):
                filename = fn
                break

    return filename


def getIndex(stroke):
    index = stroke.split('[')
    index = index[1].split(']')
    index = int(index[0])

    return index


def getGeoCoord(filename):
    coord = []
    f = open(filename)

    for line in f.readlines():
        line = line.rstrip('\n')
        line = line.split(',')
        tmp = [float(line[0]), float(line[1])]
        coord.append(tmp)

    return coord


def addPolygonToDB(name, kml_name, user, kml_path, kml_url, ds, text_kml=''):
    customer_pol = CustomerPolygons.objects.none()

    if CustomerPolygons.objects.filter(name=name).exists():
        CustomerPolygons.objects.filter(name=name).update(
            name=name,
            kml_name=kml_name,
            user=user,
            data_set=ds,
            kml_path=kml_path,
            kml_url=kml_url,
            text_kml=text_kml
        )
        customer_pol = CustomerPolygons.objects.get(
                            name=name,
                            kml_name=kml_name,
                            user=user,
                            data_set=ds,
                            kml_path=kml_path,
                            kml_url=kml_url,
                            text_kml=text_kml
                        )
    else:
        customer_pol = CustomerPolygons.objects.create(
                            name=name,
                            kml_name=kml_name,
                            user=user,
                            data_set=ds,
                            kml_path=kml_path,
                            kml_url=kml_url,
                            text_kml=text_kml
                        )

    return customer_pol


def get_parameters_customer_info_panel(data_set, shelf_data, stat_file, absolute_png_url, is_ts=False):
    # print '!!!!!!!!!!!!!!!!!!!!!!  11 shelf_data =========================== ', shelf_data
    # order_data_set = data_set.order_by('attribute_name')
    
    warning_message = ''
    tif_path = ''
    png_path = ''
    url_png = ''

    try:
        png_pref = str(shelf_data.lutfiles.lut_file).split('.txt')[0]
    except Exception, e:
        # print '!!!!!!!!!!!!!!!!! get_parameters_customer_info_panel ======================== ', e
        png_pref = 'greyscale'

    try:
        attribute_name = shelf_data.attribute_name
    except Exception:
        attribute_name = ''

    try:
        root_filename = shelf_data.root_filename
    except Exception:
        root_filename = ''

    results_directory = data_set.results_directory
    project_name = results_directory.split('/')[0]
    # year_dir = shelf_data.root_filename
    sub_dir = SUB_DIRECTORIES[stat_file]

    # print '!!!!!!!!!!!!! is_ts ========================= ', is_ts
    # print '!!!!!!!!!!!!! attribute_name ========================= ', attribute_name

    if is_ts:
        timeser_dir = ''
        try:
            files_list = []
            file_area_name = ''
            attribute_name = shelf_data
            png_pref = str(data_set.shelf_data.lutfiles.lut_file).split('.txt')[0]

            project_directory = os.path.join(PROJECTS_PATH, results_directory)
            # ts_directory = os.path.join(PROJECTS_PATH, results_directory, root_filename, sub_dir)
            pr_root, pr_dirs, pr_files = os.walk(project_directory).next()
            pr_dirs.sort()

            # print '!!!!!!!!!!!!! attribute_name ========================= ', attribute_name

            # print '!!!!!!!!!!!!!!!! project_directory ============================= ', project_directory
            # print '!!!!!!!!!!!!!!!! pr_dirs ============================= ', pr_dirs

            
            for sub_dir_1 in pr_dirs:
                if str(sub_dir_1) in attribute_name:
                    ts_directory = os.path.join(project_directory, sub_dir_1, sub_dir)
                    timeser_dir = ts_directory
                    ts_root, ts_dirs, ts_files = os.walk(ts_directory).next()
                    ts_files.sort()

                    # print '!!!!!!!!!!!!!!!! ts_directory ============================= ', ts_directory

                    # for sub_dir_2 in ts_dirs:
                    #     ts_sub_directory = os.path.join(ts_directory, sub_dir_2)
                    #     ts_sub_root, ts_sub_dirs, ts_sub_files = os.walk(ts_sub_directory).next()
                    #     ts_sub_files.sort()

                    #     print '!!!!!!!!!!!!!!!! ts_sub_directory ============================= ', ts_sub_directory


                    for f in ts_files:
                        fl, ext = os.path.splitext(f)

                        if ext == '.tif':
                            files_list.append(f)
                            break
            
                    # print '!!!!!!!!!!!!!!!! files_list ============================= ', files_list

                    if files_list:
                        file_area_name = files_list[0].split('.tif')[0]
                        tif = '{0}.tif'.format(file_area_name)
                        png = '{0}{1}.png'.format(file_area_name, png_pref)

                        tif_path = os.path.join(ts_directory, tif)
                        png_path = os.path.join(PNG_PATH, png)
                        url_png = '{0}/{1}'.format(absolute_png_url, png)
                    # break
        except StopIteration, e:
            warning_message = u'The path "{0}" does not exist.'.format(os.path.join(project_directory, attribute_name))
        except AttributeError:
            warning_message = u'Please set Shelf Data for "{0}" Dataset'.format(data_set)
        except Exception, e:
            warning_message = u'The except path "{0}" does not exist.'.format(e)
    else:
        file_area_name = '{0}_{1}.{2}'.format(stat_file, root_filename, project_name)
        tif = '{0}.tif'.format(file_area_name)
        png = '{0}{1}.png'.format(file_area_name, png_pref)

        tif_path = os.path.join(PROJECTS_PATH, results_directory, root_filename, tif)
        png_path = os.path.join(PNG_PATH, png)
        url_png = '{0}/{1}'.format(absolute_png_url, png)

    # print '!!!!!!!!!!!!! attribute_name =================== ', attribute_name

    return attribute_name, file_area_name, tif_path, png_path, url_png, warning_message


def createCustomerInfoPanel(customer, data_set, shelf_data, stat_file, absolute_png_url,
                            is_show, order=0, delete=True, is_ts=False):
    if delete:
        CustomerInfoPanel.objects.filter(user=customer).delete()

    attribute_name, file_area_name,\
    tif_path, png_path, url_png, warning_message = get_parameters_customer_info_panel(data_set,
                                    shelf_data, stat_file, absolute_png_url, is_ts)

    # print '!!!!!!!!!!!!! attribute_name =================== ', attribute_name
    # print '!!!!!!!!!!!!! tif_path =================== ', tif_path
    # print '!!!!!!!!!!!!! file_area_name =================== ', file_area_name
    # print '!!!!!!!!!!!!! tif_path =================== ', tif_path
    # print '!!!!!!!!!!!!! png_path =================== ', png_path
    # print '!!!!!!!!!!!!! url_png =================== ', url_png
    # print '!!!!!!!!!!!!! warning_message =================== ', warning_message

    info_panel = CustomerInfoPanel.objects.create(
                    user=customer,
                    data_set=data_set,
                    attribute_name=attribute_name,
                    statistic=stat_file,
                    file_area_name=file_area_name,
                    tif_path=tif_path,
                    png_path=png_path,
                    url_png=url_png,
                    order=order,
                    is_show=is_show,
                    is_ts=is_ts)
    info_panel.save()

    return info_panel, warning_message


def createKml(user, filename, info_window, url, data_set, count_color, *args):
    # Create KML file for the draw polygon
    
    outer_coord = []
    inner_coord = []
    kml_filename = str(filename) + '.kml'
    kml_url = url + '/' + kml_filename

    if not args:
        tmp_file = str(user) + '_coord_kml.txt'
        tmp_path = os.path.join(TMP_PATH, tmp_file)
        coord = getGeoCoord(tmp_path)
    else:
        outer_coord = args[0]['outer_coord'][0]
        inner_coord = args[0]['inner_coord']

        # tmp_inner_coord = []
        # len_inner_coord = len(args[0]['inner_coord'])

        # if args[0]['inner_coord']:
        #     for n in xrange(len_inner_coord):
        #         tmp_inner_coord += args[0]['inner_coord'][n]

        # inner_coord.append(tmp_inner_coord)

    # print '!!!!!!!!!!! 2 info_window ======================== ', info_window
    # print '!!!!!!!!!!! 2 outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! 2 inner_coord ======================== ', inner_coord
    # print '!!!!!!!!!!! 2 inner_coord LEN ======================== ', len(args[0]['inner_coord'])
    # print '!!!!!!!!!!! 2 args ======================== ', args
    # print '!!!!!!!!!!! 2 outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! 2 inner_coord ======================== ', inner_coord
    # print '!!!!!!!!!!! 2 info_window ======================== ', info_window
    # print '!!!!!!!!!!! COLOR ======================== ', COLOR_KML[count_color]
    # print '!!!!!!!!!!! LAST ID COUNT AOI ======================== ', cip_last_id.id
    # print '!!!!!!!!!!! %%%%%%%% ======================== ', count_color
    # print '!!!!!!!!!!! filename ======================== ', filename
    # print '!!!!!!!!!!! COORD ======================== ', coord
    # print '!!!!!!!!!!! COORD outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! COORD inner_coord ======================== ', inner_coord
    # var = 'x'
    # for i in range(10):
    #     exec(var+str(i)+' = ' + str(i))

    # len_inner_coord = len(inner_coord)
    # pol_dict = {}

    kml = simplekml.Kml()
    pol = kml.newpolygon(name=filename)

    if not args:
        pol.outerboundaryis.coords = coord
    else:
        pol.outerboundaryis = outer_coord

        if inner_coord:
            pol.innerboundaryis = inner_coord


    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # if len_inner_coord:
    #     for n in xrange(1, len_inner_coord):
    #         pol_dict['pol_'+str(n)] = kml.newpolygon(name=filename)
    # **************************************************************************
    
    # print '!!!!!!!!!!!!!!!!!! len_inner_coord =========================== ', len_inner_coord

    # if not args:
    #     pol.outerboundaryis.coords = coord
    # else:
    #     pol.outerboundaryis = outer_coord
    #     # pol_2.outerboundaryis = outer_coord
    #     # pol.innerboundaryis = inner_coord[1]

    #     if len_inner_coord:
    #         pol.innerboundaryis = inner_coord[0]

    #         for n in xrange(1, len_inner_coord):
    #             pol_dict['pol_'+str(n)].innerboundaryis = inner_coord[n]

    # **************************************************************************
    # # **************************************************************************
    # # **************************************************************************

        # inner_list.append(inner_coord[0])
        # inner_list.append(inner_coord[1])
        # pol.innerboundaryis = inner_coord
        # pol_2.innerboundaryis = inner_coord[1]

        # for n in xrange(len(inner_coord)):
        #     pol.innerboundaryis = inner_coord[n]
            
    # pol.style.linestyle.color = simplekml.Color.hex('#ffffff')
    
    # print '!!!!!!!!!!!!!!!!!! pol_dict =========================== ', pol_dict
    
    pol.style.linestyle.color = 'ffffffff'
    pol.style.linestyle.width = 2

    # pol_2.style.linestyle.color = 'ffffffff'
    # pol_2.style.linestyle.width = 2


    pol.style.polystyle.color = simplekml.Color.changealphaint(100, COLOR_HEX[count_color])
    # pol_2.style.polystyle.color = simplekml.Color.changealphaint(100, COLOR_HEX[count_color])
    # pol.style.polystyle.color = simplekml.Color.changealphaint(100, 'ff3c14dc')
    # pol.style.polystyle.color = 'ff3c14dc'

    pol.style.balloonstyle.text = info_window
    # pol_2.style.balloonstyle.text = info_window
    # pol.style.balloonstyle.bgcolor = simplekml.Color.lightgreen
    # pol.style.balloonstyle.bgcolor = simplekml.Color.red
    pol.style.balloonstyle.bgcolor = COLOR_HEX[count_color]
    pol.style.balloonstyle.textcolor = COLOR_HEX[count_color]

    # pol_2.style.balloonstyle.bgcolor = COLOR_HEX[count_color]
    # pol_2.style.balloonstyle.textcolor = COLOR_HEX[count_color]
    # pol.style.balloonstyle.textcolor = simplekml.Color.hex('#283890')

    kml_path = os.path.join(KML_PATH, user.username, kml_filename)

    # print '!!!!!!!!!!!!!!!!!! kml_path =========================== ', kml_path
    
    kml.save(kml_path)

    if inner_coord:
        testkml = ''

        with open(kml_path) as f:
            testkml = f.readlines()

        testkml = "".join(map(lambda x: x.strip(), testkml))
        tmp_line = re.sub(r"Ring><Linear", "Ring></innerBoundaryIs><innerBoundaryIs><Linear", testkml)
        list_lines = tmp_line.split('>')[0:]
        new_tmp_line = '>\n'.join(list_lines)
        my_file = open(kml_path, 'w')
        my_file.write(new_tmp_line)
        my_file.close()

        print '!!!!!!!!!!!!!!!!! kml_path 33 ============================= ', kml_path


    polygon = addPolygonToDB(filename, kml_filename, user, kml_path, kml_url, data_set, info_window)

    return polygon


def getAttributeUnits(user, show_file):
    attribute_name = 'Tree Count'
    units = '%'

    try:
        cur_attribute = CustomerInfoPanel.objects.get(
                            user=user,
                            file_area_name=show_file)
        attribute_name = cur_attribute.attribute_name
        sh_data = ShelfData.objects.filter(attribute_name=attribute_name)
        units = sh_data[0].units
    except Exception:
        pass

    return attribute_name, units


def getResultDirectory(dataset, shelfdata):
    dirs_list = []
    # is_ts = dataset.is_ts

    try:
        project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)
        root, dirs, files = os.walk(project_directory).next()
        dirs.sort()

        for sd in shelfdata:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)

        # if 'TS_' in dataset.results_directory:
        #     for dy in dirs:
        #         dirs_list.append(dy)
        #     is_ts = True
        # else:
        #     for sd in shelfdata:
        #         if str(sd.root_filename) in dirs:
        #             dirs_list.append(sd)
    except Exception, e:
        print '----->>>    Exception getResultDirectory ========================= ', e
        pass

    # print '!!!!!!!!!!!!!!!!!!!! DIRS LIST ========================= ', dirs_list
    # print '!!!!!!!!!!!!!!!!!!!! TS ========================= ', is_ts

    return dirs_list


def getTsResultDirectory(dataset):
    dirs_list = []
    shelf_data = dataset.shelf_data

    try:
        project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)
        root, dirs, files = os.walk(project_directory).next()
        dirs.sort()

        # print '!!!!!!!!!!!! project_directory ======================= ', project_directory
        # print '!!!!!!!!!!!! DIRS ======================= ', dirs

        for d in dirs:
            name = '{0} {1}'.format(shelf_data, d)
            dirs_list.append(name)

        # if 'TS_' in dataset.results_directory:
        #     for dy in dirs:
        #         dirs_list.append(dy)
        #     is_ts = True
        # else:
        #     for sd in shelfdata:
        #         if str(sd.root_filename) in dirs:
        #             dirs_list.append(sd)
    except Exception, e:
        print '----->>>    Exception getTsResultDirectory ========================= ', e
        pass

    # print '!!!!!!!!!!!!!!!!!!!! DIRS LIST ========================= ', dirs_list
    # print '!!!!!!!!!!!!!!!!!!!! TS ========================= ', is_ts

    return dirs_list


def getDataSet(ds_id, data_set):
    data_set_id = ds_id

    try:
        data_set = DataSet.objects.get(pk=data_set_id)
    except DataSet.DoesNotExist, e:
        print 'DataSet.DoesNotExist ========================= ', e
        data_set_id = int(data_set.id)

    return data_set, data_set_id


def getListTifFiles(customer, dataset):
    list_files_tif = []
    list_data_db = []
    attributes_reports = AttributesReport.objects.filter(
                            user=customer, data_set=dataset)

    # print '!!!!!!!!!!!!!!!!!!! attributes_reports ====================== ', attributes_reports

    if attributes_reports:
        if dataset.is_ts:
            attributes_reports = attributes_reports.order_by('attribute')

            for attr in attributes_reports:
                # sub_dir = attr.shelfdata.root_filename + '/' + SUB_DIRECTORIES[attr.statistic]
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory, sub_dir)
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory)

                project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)

                # print '!!!!!!!!!! sub_dir_path ========================= ', sub_dir_path
                # print '!!!!!!!!!! project_directory ========================= ', project_directory

                if os.path.exists(project_directory):
                    pr_root, pr_dirs, pr_files = os.walk(project_directory).next()
                    pr_dirs.sort()

                    # print '!!!!!!!!!! project_directory ========================= ', project_directory
                    print '!!!!!!!!!! attr.statistic ========================= ', attr.statistic

                    for pd in pr_dirs:
                        if pd in attr.attribute:
                            sub_directory = os.path.join(project_directory, pd, SUB_DIRECTORIES[attr.statistic])
                            sub_root, sub_dirs, sub_files = os.walk(sub_directory).next()
                            sub_files.sort()

                            # print '!!!!!!!!!! sub_directory ========================= ', sub_directory

                            for f in sub_files:
                                fl, ext = os.path.splitext(f)

                                if ext == '.tif':
                                    fl_tif = os.path.join(sub_directory, f)
                                    str_data_db = '{0}$$${1}$$$'.format(attr.shelfdata.id, fl_tif)

                                    list_files_tif.append(fl_tif)
                                    list_data_db.append(str_data_db)
                                    break
                            break
                    # print '!!!!!!!!!! list_data_db ========================= ', list_data_db
                    # print '!!!!!!!!!! list_files_tif ========================= ', list_files_tif
        else:
            attributes_reports = attributes_reports.order_by('shelfdata__attribute_name')

            for attr in attributes_reports:
                name_1 = attr.shelfdata.root_filename
                name_2 = dataset.results_directory.split('/')[0]
                tif_path = os.path.join(PROJECTS_PATH, dataset.results_directory, name_1)
                fl_tif = '{0}/{1}_{2}.{3}.tif'.format(tif_path, attr.statistic, name_1, name_2)
                str_data_db = '{0}$$${1}$$$'.format(attr.shelfdata.id, fl_tif)

                list_files_tif.append(fl_tif)
                list_data_db.append(str_data_db)

    # print '!!!!!!!!!! FILE ========================= ', list_files_tif
    # print '!!!!!!!!!! DATA DB ========================= ', list_data_db

    return list_files_tif, list_data_db


def addTsToDB(name, customer, data_set, customer_polygons, result_year,
                stat_code, result_date, value_of_time_series, attribute):
    if TimeSeriesResults.objects.filter(name=name, user=customer, data_set=data_set).exists():
        ts_obj = TimeSeriesResults.objects.filter(name=name).update(
            customer_polygons=customer_polygons,
            result_year=result_year, stat_code=stat_code,
            result_date=result_date,
            value_of_time_series=value_of_time_series,
            attribute=attribute
        )
    else:
        ts_obj = TimeSeriesResults.objects.create(
            name=name, user=customer, data_set=data_set,
            customer_polygons=customer_polygons,
            result_year=result_year, stat_code=stat_code,
            result_date=result_date,
            value_of_time_series=value_of_time_series,
            attribute=attribute
        )
        ts_obj.save()


def createTimeSeriesResults(aoi, file_in, file_out):
    # list_files_tif = []
    # list_data_db = []

    project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory)
    attributes_reports = AttributesReport.objects.filter(
                            user=aoi.user, data_set=aoi.data_set
                        ).order_by('attribute')
    # attributes_reports = AttributesReport.objects.filter(
    #                         user=aoi.user, data_set=aoi.data_set
    #                     ).order_by('shelfdata__attribute_name')

    # print '!!!!!!!!!!!!!!!!!! ATTRIBUTES REPORTS ================================ ', attributes_reports

    if attributes_reports:
        for attr in attributes_reports:
            result_year = (attr.attribute).split(' ')[-1]

            # result_year = attr.shelfdata.root_filename
            # sub_dir_name = SUB_DIRECTORIES[attr.statistic]
            # sub_dir = result_year + '/' + sub_dir_name
            
            project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, result_year)

            # project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, result_year)
            # project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, sub_dir)

            # print '!!!!!!! YEAR ========================== ', result_year
            # print '!!!!!!! DIR YEAR ========================== ', project_directory
            # print '!!!!!!! YES DIR YEAR ========================== ', os.path.exists(project_directory)

            # project_directory = os.path.join(sub_dir_path)

            if os.path.exists(project_directory):
                root_year, dirs_year, files_year = os.walk(project_directory).next()
                dirs_year.sort()
                # files.sort()

                for d in dirs_year:
                    sub_dir_name = d
                    project_directory_year = os.path.join(project_directory, d)
                    sub_root, sub_dirs, sub_files = os.walk(project_directory_year).next()
                    sub_dirs.sort()
                    sub_files.sort()

                    for f in sub_files:
                        fl, ext = os.path.splitext(f)

                        # print '!!!!!!! FILE ========================== ', f

                        if ext == '.tif':
                            file_ts_tif = os.path.join(project_directory_year, f)
                            
                            try:
                                ts_day = f.split(result_year+'_')[1]
                                ts_day = ts_day.split('_')[0]
                                ts_date = date(int(result_year), 1, 1)
                                ts_delta = timedelta(days=int(ts_day)-1)
                                result_date = ts_date + ts_delta
                                ts_name = '{0}_{1}_{2}_{3}'.format(aoi.name, result_year, sub_dir_name, ts_day)
                                ts_value = '0'

                                command_line_ts = '{0} {1} {2} {3}'.format(
                                                        SCRIPT_GETPOLYINFO,
                                                        file_ts_tif,
                                                        file_in,
                                                        file_out
                                                    )

                                proc_script = Popen(command_line_ts, shell=True)
                                proc_script.wait()

                                file_out_coord_open = open(file_out)

                                for line in file_out_coord_open.readlines():
                                    new_line = line.replace(' ', '')
                                    new_line = new_line.replace('\n', '')
                                
                                    # print '!!!!!!! 1 NEW LINE ========================== ', new_line

                                    if new_line:
                                        ts_value = new_line.split(',')[2]
                                        scale = attr.shelfdata.scale

                                        # print '!!!!!!! 1 NEW LINE ========================== ', new_line

                                        if scale:
                                            ts_value = str(float(ts_value) / scale)

                                        # print '!!!!!!! 2 NEW LINE ========================== ', new_line
                                        
                                addTsToDB(ts_name, aoi.user, aoi.data_set, aoi, result_year,
                                            sub_dir_name, result_date, ts_value, attr.attribute)

                                # list_files_tif.append(fl_tif)
                                # list_data_db.append(str_data_db)

                                # print '!!!!!!!!!! DAY ========================= ', ts_day
                                # print '!!!!!!!!!! DATE ========================= ', result_date
                            except IndexError:
                                pass


def getCountTs(dataset, shd):
    # print '!!!!!!!!!!!!!!!!! SHD ===================== ', shd

    is_ts = dataset.is_ts
    count_ts = 0

    path_cur_proj = dataset.results_directory
    path_to_proj = os.path.join(PROJECTS_PATH, path_cur_proj)

    # print '!!!!!!!!!!!!!!!!! path_to_proj ===================== ', path_to_proj

    try:
        if os.path.exists(path_to_proj):
            pr_root, pr_dirs, pr_files = os.walk(path_to_proj).next()
            pr_dirs.sort()

            # print '!!!!!!!!!!!!!!!!! pr_dirs ===================== ', pr_dirs


            for d in pr_dirs:
                # print '!!!!!!!!!!!!!!!!! d ===================== ', d
                # print '!!!!!!!!!!!!!!!!! IN SHD ===================== ', shd
                # print '!!!!!!!!!!!!!!!!! d in shd ===================== ', d in shd
                if d in shd:
                    path_to_subdir = os.path.join(path_to_proj, d)
                    sub_root, sub_dirs, sub_files = os.walk(path_to_subdir).next()
                    sub_dirs.sort()

                    # print '!!!!!!!!!!!!!!!!! path_to_subdir ===================== ', path_to_subdir

                    for sd in sub_dirs:
                        attr_dir = os.path.join(path_to_subdir, sd)
                        attr_root, attr_dirs, attr_files = os.walk(attr_dir).next()
                        attr_files.sort()

                        # print '!!!!!!!!!!!!!!!!! attr_dir ===================== ', attr_dir

                        for f in attr_files:
                            fl, ext = os.path.splitext(f)

                            if ext == '.tif':
                                count_ts += 1
    except Exception:
        pass

    # print '!!!!!!!!!!!!!!!!! getCountTs ===================== ', count_ts

    return count_ts


def get_count_color():
    divider = len(COLOR_HEX_NAME)
    return randint(0, divider)


# view Customer Section
@login_required
@render_to('customers/customer_section.html')
def customer_section(request):
    """**View for the "Customer section" page.**

    :Functions:
        When you load the page is loaded map with Google MAP. Initial coordinates: eLat = 0, eLng = 0.
        Zoom map is variable GOOGLE_MAP_ZOOM, whose value is in the project settings.
        Code view allows to change position when you enter values in the fields on the page "Enter Lat" and "Enter Log".

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    # PNG_DIRECTORY = 'media/png'
    # PNG_PATH = os.path.join(BASE_DIR, PNG_DIRECTORY)
    # PROJECTS_PATH = '/lustre/w23/mattgsi/satdata/RF/Projects'
    

    ####################### write log file
    log_file = '/home/gsi/LOGS/customer_section.log'
    customer_section = open(log_file, 'w+')
    now = datetime.now()
    customer_section.write('DATE: {0}\n'.format(str(now)))
    customer_section.write('USER: {0}\n'.format(str(request.user)))
    customer_section.write('\n')

    log_file_timer = '/home/gsi/LOGS/timer_script.log'
    timer_script = open(log_file_timer, 'w')
    now = datetime.now()
    timer_script.write('DATE: '+str(now))
    timer_script.write('\n')
    customer_section.write('USER: '+str(request.user))
    timer_script.write('\n')

    log_save_kml = '/home/gsi/LOGS/error_save_kml.log'
    error_save_kml = open(log_save_kml, 'a+')
    now = datetime.now()
    error_save_kml.write('DATE: '+str(now))
    error_save_kml.write('\n')
    error_save_kml.write('USER: '+str(request.user))
    error_save_kml.write('\n')
    #######################

    customer = request.user
    shelf_data_all = ShelfData.objects.all().order_by('attribute_name')
    customer_info_panel = CustomerInfoPanel.objects.filter(user=customer)
    customer_polygons = CustomerPolygons.objects.filter(user=customer)
    polygons_path = os.path.join(MEDIA_ROOT, 'kml')
    customer_access = CustomerAccess.objects.filter(user=customer)
    customer_access_ds = None
    is_convert_tif_png = False

    path_ftp_user = os.path.join(FTP_PATH, customer.username)

    # COORDINATE
    # in_ts_coord_tmp = str(customer) + '_ts_coord_tmp.kml'
    out_ts_coord_tmp = str(customer) + '_ts_coord_tmp.txt'
    in_coord_tmp = str(customer) + '_coord_tmp.kml'
    out_coord_tmp = str(customer) + '_coord_tmp.txt'
    out_coord_kml = str(customer) + '_coord_kml.txt'
    # coord_tmp = str(request.user) + '_coord_tmp.kml'
    
    # file_path_in_ts_coord_tmp = os.path.join(TMP_PATH, in_ts_coord_tmp)
    file_path_out_ts_coord_tmp = os.path.join(TMP_PATH, out_ts_coord_tmp)
    file_path_in_coord_tmp = os.path.join(TMP_PATH, in_coord_tmp)
    file_path_out_coord_tmp = os.path.join(TMP_PATH, out_coord_tmp)
    file_path_out_coord_kml = os.path.join(TMP_PATH, out_coord_kml)
    # file_path_coord = os.path.join(TMP_PATH, coord_tmp)

    # DB TMP FILES
    customer_tmp_for_db = str(customer) + '_db.csv'
    tmp_db_file = os.path.join(TMP_PATH, customer_tmp_for_db)


    if customer_access:
        customer_access_ds = CustomerAccess.data_set.through.objects.filter(
                        customeraccess_id=customer_access[0].id).order_by('dataset_id')

    url_name = 'customer_section'
    data_sets = []
    error_message = ''
    warning_message = ''

    data_set_id = 0
    polygons = []
    attribute_list_infopanel = []
    statistics_infopanel = []
    show_dataset_cip = ''
    show_image_cip = ''
    show_statistic_cip = ''
    show_report_ap = []
    file_tif_path = ''
    tab_active = 'view'
    is_time_series = False
    time_series_list = []

    # default GEOTIFF coordinates
    cLng = DAFAULT_LON
    cLat = DAFAULT_LAT
    eLat_1 = 0
    eLng_1 = 0
    eLat_2 = 0
    eLng_2 = 0
    google_map_zoom = 0.001
    url_png = ''

    # Data for the TS Diagramm
    aoi_list = []
    ts_title = ''
    ts_subtitle = ''
    ts_units = 'UNITS, ha'
    ts_aoi_name = ''
    ts_series_year = ''
    ts_stat_code = ''
    ts_data = ''
    ts_result_date = ''
    time_series_clear = False
    # ts_data = []
    # ts_data = {}
    
    select_diagram = 'line'
    select_aoi = 0.0001
    select_year = None

    # count_ts = 0

    # The url to are PNG, KML urls
    scheme = '{0}://'.format(request.scheme)
    absolute_png_url = os.path.join(scheme, request.get_host(), PNG_DIRECTORY)
    absolute_kml_url = os.path.join(scheme, request.get_host(), KML_DIRECTORY, customer.username)
    absolute_legend_url = os.path.join(scheme, request.get_host(), LEGENDS_DIRECTORY)

    # print '!!!!!!!!! START REQ ZOOM ====================== ', request.session['zoom_map']

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Get the User DataSets
    ds_id_list = []
    if customer_access_ds:
        for n in customer_access_ds:
            ds_id_list.append(n.dataset_id)
            # try:
            #     ds = DataSet.objects.get(pk=n.dataset_id)
            #     data_sets.append(ds)
            # except DataSet.DoesNotExist, e:
            #     print 'ERROR Get DataSet ==================== ', e
            #     pass
    else:
        error_message = 'You have no one DataSet for view. Please contact to the admin.'
        data = {
            'error_message': error_message
        }

        return data

    if ds_id_list:
        data_sets = DataSet.objects.filter(id__in=ds_id_list).order_by('name')
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # print '!!!!!!!!!!!!!!!!!!! 1 request.session[time_series_list] ================================== ', request.session['time_series_list']

    # GET SESSIONS
    # Get select data_set sessions
    if request.session.get('select_data_set', False):
        data_set_id = int(request.session['select_data_set'])
        # cur_cip = CustomerInfoPanel.objects.filter(user=customer)
        # data_set_id = cur_cip[0].data_set.id
    else:
        CustomerInfoPanel.objects.filter(user=customer).delete()
        request.session['select_data_set'] = data_sets[0].id
        # request.session.set_expiry(172800)

    # Get select active tab sessions
    if request.session.get('tab_active', False):
        tab_active = request.session['tab_active']
    else:
        request.session['tab_active'] = tab_active
        # request.session['time_series_view'] = False
        
    # # Get Report active
    # if request.session.get('report_list', False):
    #     report_list = request.session['report_list']
    # else:
    #     request.session['report_list'] = report_list

    # Get Time Series active
    if request.session.get('time_series_list', False):
        time_series_list = request.session['time_series_list']
    else:
        request.session['time_series_list'] = ''

    # Get Zoom Google Maps
    if request.session.get('zoom_map', False):
        google_map_zoom = request.session['zoom_map']
    else:
        request.session['zoom_map'] = google_map_zoom

    # Get Center LAT Google Maps
    if request.session.get('center_lat', False):
        cLat = request.session['center_lat']
    else:
        request.session['center_lat'] = 0.001

    # Get Center LNG Google Maps
    if request.session.get('center_lng', False):
        cLat = request.session['center_lng']
    else:
        request.session['center_lng'] = 0.001

    # Get Clear TS View
    if request.session.get('time_series_clear', False):
        time_series_clear = request.session['time_series_clear']
    else:
        request.session['time_series_clear'] = time_series_clear

    # Get Select Diagram
    if request.session.get('select_diagram', False):
        select_diagram = request.session['select_diagram']
    else:
        request.session['select_diagram'] = select_diagram

    # Get Select AOI
    if request.session.get('select_aoi', False):
        select_aoi = request.session['select_aoi']
    else:
        request.session['select_aoi'] = select_aoi

    # Get Select YEAR
    if request.session.get('select_year', False):
        select_year = request.session['select_year']
    else:
        request.session['select_year'] = select_year

    # Get Select TS
    if request.session.get('count_ts', False):
        count_ts = request.session['count_ts']
    else:
        request.session['count_ts'] = 0

    # time_series_list = ''
    
    if tab_active != 'ts':
        request.session['time_series_clear'] = False
        request.session['select_aoi'] = 0.0001
        request.session['time_series_list'] = ''
        
    

    # print '!!!!!!!!!!!!!!!!!!!! data_set_id ==================== ', data_set_id
    # print '!!!!!!!!!!!!!!!!!!!! data_set ==================== ', data_sets[0]
    # Get the DataSet and DataSet ID select
    data_set, data_set_id = getDataSet(data_set_id, data_sets[0])

    is_time_series = data_set.is_ts
    dir_l = ''

    # Get the Statistics list
    # dirs_list = getResultDirectory(data_set, shelf_data_all)

    if not is_time_series:
        dirs_list = getResultDirectory(data_set, shelf_data_all)
    else:
        dirs_list = getTsResultDirectory(data_set)
        
    # print '!!!!!!!!!!!!!!!!!!!! dirs_list ==================== ', dirs_list

    if dirs_list:
        dir_l = dirs_list[0]
    else:
        dir_l = ''

    cip_is_show = CustomerInfoPanel.objects.filter(
                                user=customer,
                                is_show=True)
    if not cip_is_show:
        new_cip, warning_message = createCustomerInfoPanel(
                        customer, data_set, dir_l, 'mean_ConditionalMean',
                        absolute_png_url, True, order=0, is_ts=is_time_series
                    )
        if warning_message:
            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_section'),
                (warning_message)))

    # get AJAX POST for KML files
    if request.is_ajax() and request.method == "POST":
        data_post_ajax = request.POST
        data = ''

        # print '!!!!!!!!!!!!!!!!! data_post_ajax ===================== ', data_post_ajax
        # print '!!!!!!!!!!!!!!!!! data_post_ajax LIST ===================== ', data_post_ajax.lists()
        # print '!!!!!!!!!!!!!!!!! ts_list ===================== ', data_post_ajax['ts_list']
        # print '!!!!!!!!!!!!!!!!! ts_list ===================== ', ('ts_list[]' in data_post_ajax)
        # print '!!!!!!!!!!!!!!!!! BUTTON ===================== ', 'button' in data_post_ajax


        if 'button' in data_post_ajax and (data_post_ajax['button'] == 'next' or data_post_ajax['button'] == 'previous'):
            try:
                if 'zoom_map' in data_post_ajax:
                    request.session['zoom_map'] = data_post_ajax['zoom_map']
                    request.session['center_lat'] = data_post_ajax['center_lat']
                    request.session['center_lng'] = data_post_ajax['center_lng']

                    # print '!!!!!!!!!! CENTER LAT =================== ', request.session['center_lat']
                    # print '!!!!!!!!!! CENTER LNG =================== ', request.session['center_lng']

                if 'attr_list[]' in data_post_ajax:
                    if not 'stat_list[]' in data_post_ajax:
                        statistics_viewlist = ['mean_ConditionalMean']
                    else:
                        statistics_viewlist = data_post_ajax.getlist('stat_list[]')

                    attributes_viewlist = data_post_ajax.getlist('attr_list[]')

                    # print 'attributes_viewlist ========================= ', attributes_viewlist
                    # print 'statistics_viewlist ========================= ', statistics_viewlist

                    count_obj = len(attributes_viewlist) * len(statistics_viewlist) - 1
                    is_show = False
                    new_order = 0
                    show_order = 0
                    show_attribute_name = ''
                    show_statistics_name = ''
                    is_show_sip = CustomerInfoPanel.objects.filter(
                                    user=customer, is_show=True)

                    if is_show_sip:
                        show_attribute_name = is_show_sip[0].attribute_name
                        show_statistics_name = is_show_sip[0].statistic

                    # print '!!!!!!!!!!!!!!!! show_attribute_name ========================= ', show_attribute_name
                    # print 'CIP count_obj ========================= ', count_obj
                    # print 'CIP ORDER ========================= ', is_show_sip[0].order
                    # print 'show_statistics_name ========================= ', show_statistics_name

                    CustomerInfoPanel.objects.filter(user=customer).delete()

                    for attr in attributes_viewlist:
                        try:
                            if is_time_series:
                                attr_id = attr.split('view_')[1]
                                shelf_data = attr_id
                            else:
                                attr_id = int(attr.split('view_')[1])
                                shelf_data = ShelfData.objects.get(id=int(attr_id))

                            # print '!!!!!!!!!! shelf_data ========================= ', shelf_data
                            # print '!!!!!!!!!! attr_id ========================= ', attr_id

                            is_time_series = data_set.is_ts

                            for st in statistics_viewlist:
                                createCustomerInfoPanel(customer, data_set, shelf_data,
                                                        st, absolute_png_url,
                                                        False, order=new_order, delete=False, is_ts=is_time_series)


                                if is_time_series:
                                    pass
                                    if show_attribute_name == shelf_data and show_statistics_name == st:
                                        if data_post_ajax['button'] == 'next':
                                            show_order = new_order + 1
                                        elif data_post_ajax['button'] == 'previous':
                                            show_order = new_order - 1
                                else:
                                    if show_attribute_name == shelf_data.attribute_name and show_statistics_name == st:
                                        if data_post_ajax['button'] == 'next':
                                            show_order = new_order + 1
                                        elif data_post_ajax['button'] == 'previous':
                                            show_order = new_order - 1

                                new_order += 1
                                # print '**************************************************************************************'
                                # print 'show_attribute_name ========================= ', show_attribute_name
                                # print 'shelf_data.attribute_name ========================= ', shelf_data.attribute_name
                                # print ''
                                # print 'show_statistics_name ========================= ', show_statistics_name
                                # print 'statistics ========================= ', st
                                # print '!!!!!!!!!!!!! show_order ========================= ', show_order
                                # print '**************************************************************************************'
                        except ShelfData.DoesNotExist, e:
                            print '!!!!!!!!!!!! ShelfData.DoesNotExist ========================= ', e
                            pass

                    if is_show_sip:
                        if show_order > count_obj:
                            show_order = 0
                        elif show_order < 0:
                            show_order = count_obj
                        CustomerInfoPanel.objects.filter(user=customer, order=show_order).update(is_show=True)
                    else:
                        CustomerInfoPanel.objects.filter(user=customer, order=0).update(is_show=True)

                    # try:
                    #     show_cip = CustomerInfoPanel.objects.get(user=customer, is_show=True)
                    #     data = '{0}${1}${2}'.format(show_cip.data_set.name, show_cip.attribute_name, show_cip.statistic)
                    # except CustomerInfoPanel.DoesNotExist:
                    #     pass

                    # not_show_cip = CustomerInfoPanel.objects.filter(user=customer, is_show=False)
                    #
                    # for n in not_show_cip:
                    #     try:
                    #         os.remove(n.png_path)
                    #     except Exception, e:
                    #         print '!!!!!!!!!!! ERROR =================== ', e
                    #         pass
                    #
                    # print '!!!!!!!!!!! NEXT PREW =================== '

                    return HttpResponse(data)
                elif 'attr_list[]' in data_post_ajax or not 'stat_list[]' in data_post_ajax:
                    is_time_series = data_set.is_ts

                    createCustomerInfoPanel(customer, data_set, dirs_list[0],
                                            'mean_ConditionalMean', absolute_png_url,
                                            True, order=0, is_ts=is_time_series)
            except Exception, e:
                print '!!!!!!!!!! ERROR NEXT ======================= ', e
                ####################### write log file
                customer_section.write('ERROR ATTR & STAT LIST: {0}\n'.format(e))
                ####################### write log file

            return HttpResponse(data)

        if 'ts_list[]' in data_post_ajax:
            ts_ids = data_post_ajax.getlist('ts_list[]')
            request.session['time_series_list'] = data_post_ajax.getlist('ts_list[]')
            ts_diagram = TimeSeriesResults.objects.filter(id__in=ts_ids)
            request.session['time_series_clear'] = False
            # time_series_view = True
            
            # print '!!!!!!!!!!!!!!!!! ts_list[] request.session[time_series_list] ============================== ', request.session['time_series_list']
            # print '!!!!!!!!!!!!!!!!! TS VIEW 1 ============================== ', ts_ids
            # print '!!!!!!!!!!!!!!!!! TS LIST 2 ============================== ', data_post_ajax.getlist('ts_list[]')
            
        # if 'select_diagram' in data_post_ajax:
        #     request.session['select_diagram'] = data_post_ajax['select_diagram']

        if 'button' in data_post_ajax:
            if data_post_ajax['button'] == 'draw_plot':
                if 'ts_list[]' in data_post_ajax:
                    ts_ids = data_post_ajax.getlist('ts_list[]')
                    request.session['time_series_list'] = data_post_ajax.getlist('ts_list[]')
                    ts_diagram = TimeSeriesResults.objects.filter(id__in=ts_ids)
                    request.session['time_series_clear'] = False

                if 'select_diagram' in data_post_ajax:
                    request.session['select_diagram'] = data_post_ajax['select_diagram']

                if 'select_aoi[]' in data_post_ajax:
                    print '!!!!!!!!!!!!! select_aoi[] ========================== ', data_post_ajax.getlist('select_aoi[]')
                    request.session['select_aoi'] = data_post_ajax.getlist('select_aoi[]')
                else:
                    # print '!!!!!!!!!!!!! NO select_aoi[] ========================== '
                    request.session['select_aoi'] = 0.0001

        if 'coordinate_list[0][]' in data_post_ajax:
            #################### START TIME.TIME
            startTime_start = time.time()
            #################### START TIME.TIME

            reports_cip = ShelfData.objects.none()
            cur_ds = DataSet.objects.get(id=data_set_id)
            is_time_series = cur_ds.is_ts
            statistic = ''
            data = ''
            error_msg = ''

            # print '!!!!!!!!!!!!! 22 COORD data_post_ajax ====================== ', data_post_ajax

            if 'reports[]' in data_post_ajax:
                count_ts = 0
                # request.session['count_ts'] = 0
                reports_ids = []
                # is_time_series = cur_ds.is_ts

                for rep_id in data_post_ajax.getlist('reports[]'):
                    reports_ids.append(rep_id.split('report_')[1])

                # print '!!!!!!!!!!!!! 22 reports_ids ====================== ', reports_ids

                if is_time_series:
                    reports_cip = reports_ids

                    for rs in reports_cip:
                        count_ts += getCountTs(cur_ds, rs)
                else:
                    reports_cip = ShelfData.objects.filter(
                                id__in=reports_ids).order_by('attribute_name')

                # print '!!!!!!!!!!!!! 22 reports_cip ====================== ', reports_cip

                # reports_cip = ShelfData.objects.filter(
                #                 id__in=reports_ids).order_by('attribute_name')

                # print '!!!!!!!!!!!!!!!!! 12 request count_ts =========================== ', request.session['count_ts']

                

                request.session['count_ts'] = count_ts

                # print '!!!!!!!!!!!!!!!!! 2 request count_ts =========================== ', request.session['count_ts']
                # print '!!!!!!!!!!!!!!!!! COUNT TS =========================== ', count_ts
            else:
                reports_cip = dirs_list

            if 'stats[]' in data_post_ajax:
                for stat in data_post_ajax.getlist('stats[]'):
                    statistic = stat

            # print '!!!!!!!!!!!!! statistic ====================== ', statistic
            # print '!!!!!!!!!!!!! reports_cip ====================== ', reports_cip

            AttributesReport.objects.filter(user=customer).delete()
            cips = CustomerInfoPanel.objects.filter(user=customer)

            try:
                os.remove(file_path_in_coord_tmp)
                os.remove(file_path_out_coord_tmp)
                os.remove(file_path_out_coord_kml)
                os.remove(file_path_out_ts_coord_tmp)

                os.remove(tmp_db_file)
                # os.remove(ajax_file)
                # os.remove(file_path_coord)
            except Exception, e:
                ####################### write log file
                customer_section.write('ERROR DELETE TMP FILES: {0}\n'.format(e))
                ####################### write log file
                pass

            for cip in cips:
                cip.statistic = statistic
                cip.save()

            for rs in reports_cip:
                if is_time_series:
                    attribute_report = AttributesReport.objects.create(
                                            user=customer,
                                            data_set=data_set,
                                            shelfdata=cur_ds.shelf_data,
                                            statistic=statistic,
                                            attribute=rs
                                        )
                else:
                    attribute_report = AttributesReport.objects.create(
                                            user=customer,
                                            data_set=data_set,
                                            shelfdata=rs,
                                            statistic=statistic,
                                            attribute=rs
                                        )
            
            kml_file_coord = open(file_path_out_coord_kml, "w")
            tmp = {}
            coord_dict = {}
            points_coord = []

            for n in data_post_ajax.lists():
                if n[0] != 'csrfmiddlewaretoken' and n[0] != 'reports[]' and n[0] != 'stats[]':
                    index = getIndex(n[0])
                    tmp[index] = n[1]

            for k in sorted(tmp.keys()):
                coord_dict[k] = tmp[k]

            for n in coord_dict:
                str_coord = '{0},{1}\n'.format(coord_dict[n][0], coord_dict[n][1])
                # print '!!!!!!!!!!! COORD =================== ', coord_dict[n]
                kml_file_coord.write(str_coord)
                points_coord.append(tuple(coord_dict[n]))

            # print '!!!!!!!!!!! file_path_out_coord_kml =================== ', file_path_out_coord_kml
            # print '!!!!!!!!!!! COORD =================== ', points_coord

            kml_file_coord.close()

            # *************************************************************************************************
            kml_name ='{0} {1} AREA COORDINATE'.format(request.user, data_set)
            kml = simplekml.Kml()
            kml.newpoint(name=kml_name, coords=points_coord)  # lon, lat, optional height
            kml.save(file_path_in_coord_tmp)
            list_file_tif, list_data_db = getListTifFiles(customer, data_set)

            ###################### LOG
            customer_section.write('LIST TIF FILES: {0}\n'.format(list_file_tif))
            customer_section.write('LIST DATA DB: {0}\n'.format(list_data_db))
            ###################### LOG
            
            # print '!!!!!!! list_file_tif ========================== ', list_file_tif
            # print '!!!!!!! list_data_db ========================== ', list_data_db

            # try:
            count_data = 0
            new_line = ''
            db_file_open = open(tmp_db_file, 'w')

            print '!!!!!!!!!!!!!!! list_file_tif =========================== ', list_file_tif
            print '!!!!!!!!!!!!!!! list_data_db =========================== ', list_data_db

            # if not list_file_tif:
            #     data = 'Please add the GEO data to create the report.'
            #     return HttpResponse(data)

            for file_tif in list_file_tif:
                shd_id = list_data_db[count_data].split('$$$')[0]
                scale = ShelfData.objects.get(id=shd_id).scale
                command_line_ts = ''

                # print '!!!!!!! SCALE ========================== ', scale
                # file_path_out_ts_coord_tmp
                
                #################### 2 START TIME.TIME
                startTime_script_start = time.time()
                #################### START TIME.TIME

                command_line = '{0} {1} {2} {3}'.format(
                                    SCRIPT_GETPOLYINFO,
                                    file_tif,
                                    file_path_in_coord_tmp,
                                    file_path_out_coord_tmp
                                )

                # print '!!! COMMAND LINE =========================== ', command_line
                # print '!!! FILE =========================== ', f_tif
                proc_script = Popen(command_line, shell=True)
                proc_script.wait()
                # time.sleep(1)
                
                #################### END 2 START TIME.TIME
                startTime_script_end = time.time() - startTime_script_start
                # data = startTime_script_end
                # return HttpResponse(data)
                
                print '!!!!!!!!!!!!!! TIME GETPOLYINFO SCRIPT =================== ', startTime_script_end
                timer_script.write('ONE TIME GETPOLYINFO SCRIPT: {0}\n'.format(startTime_script_end))
                #################### START TIME.TIME
                #
                #if os.path.exists(file_path_out_coord_tmp):

                if os.path.exists(file_path_out_coord_tmp):
                    file_out_coord_open = open(file_path_out_coord_tmp)

                    for line in file_out_coord_open.readlines():
                        new_line = line.replace(' ', '')
                        new_line = new_line.replace('\n', '')
                        new_line = new_line.replace(',', '$$$')

                    
                        # print '!!!!!!! 1 NEW LINE ========================== ', new_line

                        if new_line:
                            new_line = new_line.split('$$$')[1:]
                            total_aoi = int(new_line[2])
                            units_per_hectare_aoi = float(new_line[0])
                            new_line[0] = '{0:,}'.format(units_per_hectare_aoi).replace(',', ',')
                            new_line[2] = '{0:,}'.format(total_aoi).replace(',', ',')
                            # new_line[2] = str(total_aoi)

                            # print '!!!!!!! TOTAL========================== ', total_aoi
                            # print '!!!!!!! [0] NEW LINE ========================== ', new_line[0]
                            # print '!!!!!!! [2] NEW LINE ========================== ', new_line[2]

                            if scale:
                                new_line[1] = str(float(new_line[1]) / scale)

                            # print '!!!!!!! 3 NEW LINE ========================== ', new_line
                            # print '!!!!!!! 2 count_data ========================== ', count_data
                            # print '!!!!!!! 3 list_data_db[count_data] ========================== ', list_data_db[count_data]
                            # print '!!!!!!! 2 list_data_db ========================== ', list_data_db

                            new_line = '$$$'.join(new_line)
                            str_db_file = '{0}{1}'.format(list_data_db[count_data], new_line) 
                            db_file_open.write('{0}\n'.format(str_db_file))
                            count_data += 1
                            # print '!!!!!!! 3 NEW LINE ========================== ', new_line
                            # print '!!!!!!! str_DB_file ========================== ', str_db_file
                else:
                    error_msg = 'Exiting due to invalid format geotiff image (expects GDT_Int16)'
            
            db_file_open.close()
            # except Exception, e:
            #     ####################### write log file
            #     customer_section.write('ERROR CREATE KML FILES: {0}\n'.format(e))
            #     ####################### write log file
            #     print '!!!! ERROR ALL ======================= ', e
            #     pass

            # *************************************************************************************************

            # print '!!!!!!!!!!! LIST F ======================== ', list_file_tif
            # print '!!!!!!!!!!! LIST DB ======================== ', list_data_db
            # print '!!!!!!!!!!! POINTS_coord ======================== ', points_coord
            
            #################### END START TIME.TIME
            startTime_end = time.time() - startTime_start

            timer_script.write('ALL TIME CUSTOMER SECTION: {0}\n'.format(startTime_end))
            #################### START TIME.TIME
            
            print '!!!!!!!!!!!!!! TIME =================== ', startTime_end
            # print '!!!!!!!!!!!!!! error_msg =================== ', error_msg
            

            # data = count_ts
            # data = {
            #     'count_ts': count_ts,
            #     'error_msg': error_msg
            # }

            return HttpResponse(json.dumps({'count_ts': count_ts, 'error_msg': error_msg}))

            # return HttpResponse(data, error_msg)

        if 'cur_run_id' in data_post_ajax:
            # message = u'Are you sure you want to remove this objects:'
            arrea = data_post_ajax['cur_run_id']
            data = u'Are you sure you want to remove this objects: <b>"{0}"</b>?'.format(arrea)

            return HttpResponse(data)
        else:
            return HttpResponse(data)

    # get AJAX GET
    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get_ajax = request.GET
        cip = CustomerInfoPanel.objects.filter(user=customer)

        # print '!!!!!!!!!!!!!! AJAX GET ========================= ', data_get_ajax

        # print 'GET customer_section ====================== ', data_get_ajax['datasets_id']
        if 'regenerate_legend' in data_get_ajax:
            # active_cip = cip.get(is_show=True)
            is_convert_tif_png = True

        if 'clear_ts' in data_get_ajax:
            request.session['time_series_clear'] = True
            request.session['select_diagram'] = 'line'
            request.session['select_aoi'] = 0.0001

            print '!!!!!!!!!!!!!! AJAX GET CLEAR ========================= ', time_series_clear

            return HttpResponse(data)

        if 'zoom' in data_get_ajax:
            # active_cip = cip.get(is_show=True)
            request.session['zoom_map'] = data_get_ajax['zoom']
            data = request.session['zoom_map']

            return HttpResponse(data)


        # When user celect a new DataSet, the previous celected DataSet to remove
        if 'datasets_id' in data_get_ajax:
            request.session['select_data_set'] = data_get_ajax['datasets_id']
            data_set_id = request.session['select_data_set']
            request.session['zoom_map'] = 0.001
            request.session['center_lat'] = 0.001
            request.session['center_lng'] = 0.001
            request.session['select_aoi'] = 0.0001
            request.session['time_series_clear'] = False

            request.session['tab_active'] = 'view'
            # request.session['time_series_view'] = False
            tab_active = request.session['tab_active']
            # request.session['time_series_list'] = [m.id for m in TimeSeriesResults.objects.filter(
            #                                         user=customer, data_set__id=data_set_id)]
            request.session['time_series_list'] = ''
            # time_series_view = request.session['time_series_view']
            
            # print '!!!!!!!!! CIP ====================== ', cip
            
            for ip in cip:
                # print '!!!!!!!!! png_path ====================== ', ip.png_path
                # print '!!!!!!!!! legend_path ====================== ', ip.legend_path
                # remove_files(ip.png_path)
                # remove_files(ip.legend_path)

                try:
                    os.remove(ip.png_path)
                except Exception, e:
                    print '!!!!!!! ERROR remove file png ===================== ', e
                    pass

                try:
                    os.remove(ip.legend_path)
                except Exception, e:
                    print '!!!!!!! ERROR remove file legend ===================== ', e
                    pass

            status = check_current_dataset(request, data_get_ajax)

            # if request.session.get('select_data_set', False):
            #     data_set_id = int(request.session['select_data_set'])
            # else:
            #     request.session['select_data_set'] = data_sets[0].id
            #     data_set_id = request.session['select_data_set']

            # print 'data_set_id REQ ========================== ', request.session['select_data_set']
            # print '!!!!!!!!!! data_set_id ========================== ', data_set_id
            # print '!!!!!!!!!! data_sets ========================== ', data_sets[0]

            if status:
                data_set, data_set_id = getDataSet(data_set_id, data_sets[0])
                # dirs_list = getResultDirectory(data_set, shelf_data_all)
                statistic = 'mean_ConditionalMean'
                is_show = True
                is_time_series = data_set.is_ts

                if not is_time_series:
                    dirs_list = getResultDirectory(data_set, shelf_data_all)
                else:
                    dirs_list = getTsResultDirectory(data_set)

                # print '!!!!!!!!!!!!!!!!!!!! DIRRR LISTTT ============================ ', dirs_list

                if dirs_list:
                    info_panel = createCustomerInfoPanel(
                                    customer, data_set, dirs_list[0], statistic,
                                    absolute_png_url, is_show, is_ts=is_time_series
                                )
                else:
                    data = 'error'
                    # print 'ERRRRRRRRRRRRRRRRRRRRRRRROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    
            # data = request.session['zoom_map']

            # print '!!!!!!!!! REQ ZOOM ====================== ', request.session['zoom_map']

            return HttpResponse(data)

        if 'cur_area' in data_get_ajax:
            # print 'POL ========================================= ', data_get_ajax.get('cur_area', '')
            polygon_id = data_get_ajax.get('cur_area', '')
            try:
                select_area = CustomerPolygons.objects.get(pk=polygon_id)
                data = '{0}${1}'.format(select_area.name, polygon_id)
            except CustomerPolygons.DoesNotExist:
                data = 'There is no such polygon.'

            return HttpResponse(data)

        if 'polygon' in data_get_ajax:
            try:
                # polygon = data_get_ajax.get('polygon', '')
                select_polygon = CustomerPolygons.objects.none()
                poly_id = data_get_ajax.get('polygon', '')
                polygon_text = ''
                polygon_id = ''

                if CustomerPolygons.objects.filter(id=poly_id).exists():
                    select_polygon = CustomerPolygons.objects.get(id=poly_id)
                    polygon_id = 'close_' + str(select_polygon.id)

                    # print '!!!!!!!!!!!!!!! NAME ===================== ', select_polygon.name

                    if select_polygon.text_kml:
                        polygon_text += '<span class="close" id="{0}" onclick="closeIF();">&times;</span>'.format(polygon_id);
                        polygon_text += str(select_polygon.text_kml)
                    else:
                        polygon_text += 'false'

                # data = os.path.join(absolute_kml_url, polygon)

                # if request.get_host() == '127.0.0.1:8000':
                #     data = 'http://indy4.epcc.ed.ac.uk/media/kml/tree-count-1.kml'
                # else:
                #     # data = os.path.join(absolute_kml_url, select_polygon)
                #     data = select_polygon.kml_url

                data = select_polygon.kml_url

                # url_kml = 'https://doc-0s-b8-docs.googleusercontent.com/docs/securesc/t2e26pal3cvqhgci00iokqk6s7mn29k8/npdqs37ivknd5no63g2s59sujo7ea4cq/1508486400000/08805881789186013635/08805881789186013635/0B306OTCpD7KOOGpLRmUxMFo0eHc?e=download&gd=true&access_token=ya29.Gl3qBI_oyJOnMvXyhievRlD-Ir3mcdjWDBxVaZUT0ECADsYKqcqLxlljpQVJt5EOspboz53JzNPu_w5XwsEpc19Cy1p-WZTpPPvzyqz3uT465cmw4pyrhQf6fkBaypk'
                # url_kml = 'http://indy4.epcc.ed.ac.uk/media/kml/Scotland.kml'
                # data = url_kml
                # print '!!!!!!!!!!!!!!! DATA URL =================== ', data

                data += '$$$' + polygon_text + '$$$' + str(polygon_id)
                # data += polygon_text
            except Exception, e:
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!! AOI ERROR ============================ ', e
                # ############ WRITE LOG ##############################
                customer_section.write('AOI ERROR: '+str(e))
                customer_section.write('\n')
                # ############ WRITE LOG ##############################
            return HttpResponse(data)

        if 'tab_active' in data_get_ajax:
            data = request.session['tab_active']
            tab_active = data_get_ajax.get('tab_active', '')
            request.session['tab_active'] = tab_active

            # print '!!!!!!!!!!!!!!!!!!! tab_active ================================ ', tab_active

            return HttpResponse(data)

    if request.method == "POST":
        data_post = request.POST

        # print '!!!!!!!!!!!! POST ====================== ', data_post

        if 'load_button' in data_post:
            path_ftp_user = os.path.join(FTP_PATH, customer.username)

            if not os.path.exists(path_ftp_user):
                os.makedirs(path_ftp_user, 0755);

            try:
                load_file_name = str(request.FILES['upload_file_customer']).decode('utf-8')
                load_file_path = os.path.join(path_ftp_user, load_file_name)
                handle_uploaded_file(request.FILES['upload_file_customer'], load_file_path)

                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse('files_lister'),
                    (u'The file "{0}" is loaded'.format(load_file_name))))
            except MultiValueDictKeyError:
                return HttpResponseRedirect(u'%s?warning_message=%s' % (
                    reverse('customer_section'),
                    (u'Please select a file to upload to the server!')))

        if 'save_area' in data_post:
            # print '!!!!!!!!!!!!! SAVE AREA ========================='

            try:
                count_color = get_count_color()

                # print '!!!!!!!!!!!!!!! divider ===================== ', divider
                # print '!!!!!!!!!!!!!!! count_color ===================== ', count_color
                # print '!!!!!!!!!!!!!!! HEX NAME ===================== ', COLOR_HEX_NAME[count_color]

                data_kml = data_post.lists()
                area_name = ''
                total_area = ''
                attribute = []
                value = []
                units = []
                total = []
                statistic = ''

                root_filename = []

                for item in data_kml:
                    # total_area
                    if 'total_area' in item:
                        total_area = item[1][0]

                    if 'area_name' in item:
                        area_name = item[1][0].replace(' ', '-')

                    if 'attribute' in item:
                        attribute = item[1]

                    if 'value' in item:
                        value = item[1]

                    if 'units' in item:
                        units = item[1]

                    if 'total' in item:
                        total = item[1]

                    if 'statistic' in item:
                        statistic = item[1][0]

                len_attr = len(attribute)
                
                # info_window = '<h4 align="center" style="color:darkgreen;"><b>Attribute report: {0}</b></h4>\n'.format(area_name)
                info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(COLOR_HEX_NAME[count_color], area_name)
                info_window += '<p align="center"><span><b>Total Area:</b></span> ' + total_area + ' ha</p>';

                if statistic:
                    info_window += '<p align="center"><span><b>Values:</b></span> ' + statistic + '</p>';
                # info_window += '<p align="left"><font size="2">{0}: {1} ha</p></font>\n'.format(ATTRIBUTES_NAME[0], total_area)

                info_window += '<div style="overflow:auto;" class="ui-widget-content">'
                
                # if len_attr >= 8:
                #     info_window += '<div style="height:400px;overflow:scroll;" class="ui-widget-content">'
                # else:
                #     info_window += '<div style="overflow:auto;" class="ui-widget-content">'
                #     
                #     Aqua

                info_window += '<table border="1" cellspacing="5" cellpadding="5" style="border-collapse:collapse;border:1px solid black;width:100%;">\n'
                # info_window += '<caption align="left" style="margin-bottom:15px"><span><b>Total Area:</b></span> ' + total_area + ' ha</caption>'
                info_window += '<thead>\n'
                info_window += '<tr bgcolor="#CFCFCF">\n'
                info_window += '<th align="left" style="padding:10px">Attribute</th>\n'
                info_window += '<th style="padding:10px">Units per Hectare</th>\n'
                info_window += '<th style="padding:10px">Units</th>\n'
                info_window += '<th style="padding:10px">Total</th>\n'
                info_window += '</tr>\n'
                info_window += '</thead>\n'
                info_window += '<tbody>\n'

                for n in xrange(len_attr):
                    if n % 2 == 0:
                        info_window += '<tr bgcolor="#F5F5F5">\n'
                    else:
                        info_window += '<tr>';

                    info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attribute[n])
                    info_window += '<td style="padding:10px">{0}</td>\n'.format(value[n])
                    info_window += '<td style="padding:10px">{0}</td>\n'.format(units[n])
                    info_window += '<td style="padding:10px">{0}</td>\n'.format(total[n])
                    info_window += '</tr>\n'

                    # ts_root_filename = ShelfData.objects.get(attribute_name=attribute[n]).root_filename
                    # root_filename.append(ts_root_filename)

                info_window += '</tbody>\n'
                info_window += '</table>\n'
                info_window += '</div>'

                # Create KML file for the draw polygon
                ds = DataSet.objects.get(pk=data_set_id)

                cur_polygon = createKml(request.user, area_name, info_window, absolute_kml_url, ds, count_color)

                # print '!!!!!!!!! STAT ======================== ', statistic

                for n in xrange(len_attr):
                    if not DataPolygons.objects.filter(user=request.user, data_set=data_set,
                        customer_polygons=cur_polygon, attribute=attribute[n]).exists():
                            DataPolygons.objects.create(
                                user=request.user,
                                customer_polygons=cur_polygon,
                                data_set=data_set,
                                attribute=attribute[n],
                                statistic=statistic,
                                value=value[n],
                                units=units[n],
                                total=total[n],
                                total_area=total_area+' ha'
                            )
                    elif DataPolygons.objects.filter(user=request.user, data_set=data_set,
                        customer_polygons=cur_polygon, attribute=attribute[n]).exists():
                            DataPolygons.objects.filter(user=request.user, data_set=data_set,
                                customer_polygons=cur_polygon, attribute=attribute[n]
                            ).update(
                                # attribute=attribute[n],
                                statistic=statistic,
                                value=value[n],
                                units=units[n],
                                total=total[n],
                                total_area=total_area+' ha'
                            )

                # GET DATA FOR THE TIME SERIES
                if data_set.is_ts:
                    # file_path_in_coord_tmp,
                    # file_path_out_ts_coord_tmp
                    createTimeSeriesResults(cur_polygon, file_path_in_coord_tmp,
                                            file_path_out_ts_coord_tmp)
                    # ts_path = os.path.join(PROJECTS_PATH, data_set.results_directory)

                    # print '!!!!!!!!!!!!!!! root_filename ======================= ', root_filename
            except Exception, e:
                print '!!!!!!!!!!!!!!!!!!!! ERROR GEO =========================== ', e

                ###########   log ###############################################################
                error_save_kml.write('ERROR GEO: {0}\n'.format(e))
                error_save_kml.close()
                ############################################################################

                return HttpResponseRedirect(u'%s?danger_message=%s' % (
                            reverse('customer_section'),
                            (u'Please add the GEO data to create Time Series.')))
                
            # return redirect('customer_section')

        if 'delete_button' in data_post:
            kml_file = data_post.get('delete_button')
            cur_area = CustomerPolygons.objects.filter(kml_name=kml_file)
            # cur_area = get_object_or_404(
                #     CustomerPolygons, kml_name=kml_file)

            if cur_area:
                ftp_kml = os.path.join(path_ftp_user, cur_area[0].kml_name)

                try:
                    os.remove(cur_area[0].kml_path)
                except OSError:
                    pass

                try:
                    os.remove(ftp_kml)
                except Exception:
                    pass
                
                cur_data_polygons = DataPolygons.objects.filter(
                                        customer_polygons=cur_area[0]
                                    )
                
                for data_pol in cur_data_polygons:
                    data_pol.delete()

                cur_area[0].delete()

            return HttpResponseRedirect(u'%s' % (reverse('customer_section')))

        if 'area_name' in data_post:
            area_id = data_post.get('save_area_name', '')

            # print 'area_id ======================================== ', area_id

            # path_ftp_user

            if area_id:
                old_area = CustomerPolygons.objects.get(pk=area_id)
                new_area_name = data_post.get('area_name')
                new_area_name = new_area_name.replace(' ', '-')
                new_kml_name = str(new_area_name) + '.kml'
                old_path = old_area.kml_path
                new_path = os.path.join(KML_PATH, new_kml_name)
                new_kml_url = os.path.join(absolute_kml_url, new_kml_name)

                old_ftp_kml = os.path.join(path_ftp_user, old_area.kml_name)
                new_ftp_kml = os.path.join(path_ftp_user, new_kml_name)

                try:
                    os.rename(old_path, new_path)
                except Exception:
                    pass

                try:
                    os.rename(old_ftp_kml, new_ftp_kml)
                except Exception:
                    pass

                area = CustomerPolygons.objects.filter(pk=area_id).update(
                            name=new_area_name,
                            kml_url=new_kml_url,
                            kml_name=new_kml_name,
                            kml_path=new_path)

                return HttpResponseRedirect(u'%s' % (reverse('customer_section')))

    customer_info_panel = CustomerInfoPanel.objects.filter(user=customer)

    # if not customer_info_panel and dirs_list:
    #     attribute_list_infopanel.append(dirs_list[0].attribute_name)
    #     statistics_infopanel.append('mean_ConditionalMean')
    #     current_area_image = ''
    if customer_info_panel and dirs_list:
        cip = customer_info_panel.filter(user=customer).order_by('attribute_name')

        for n in cip:
            attribute_list_infopanel.append(n.attribute_name)
            statistics_infopanel.append(n.statistic)


    # Get the polygons list from media folder
    polygons = CustomerPolygons.objects.filter(
                    user=request.user,
                    data_set=data_set
                )

    if customer_info_panel:
        is_lutfile = False

        try:
            customer_info_panel_data = CustomerInfoPanel.objects.filter(
                                        user=request.user,
                                        is_show=True)

            # remove_png_file = CustomerInfoPanel.objects.filter(
            #                             user=request.user)

            # for rm_f in remove_png_file:
            #     try:
            #         os.remove(rm_f.png_path)
            #     except OSError:
            #         pass
                    
            if customer_info_panel_data:
                cip_choice = customer_info_panel_data[0]
                data_set = cip_choice.data_set
                dataset_root = data_set.results_directory
                file_tif = cip_choice.tif_path
                file_png = cip_choice.png_path
                url_png = cip_choice.url_png
                file_area_name = cip_choice.file_area_name
                attribute_name = cip_choice.attribute_name

                project_root_path = os.path.join(PROJECTS_PATH, dataset_root)
                attr_dict = {}

                # print '!!!!!!!!!!!! FILE TIF =========================== ', file_tif
                
                # *************** COLOR EACH IMAGES ***************************************************************
                try:
                    if data_set.is_ts:
                        shelf_data_attr = data_set.shelf_data
                    else:
                        shelf_data_attr = ShelfData.objects.get(attribute_name=attribute_name)

                    if shelf_data_attr.lutfiles:
                        lut_file = shelf_data_attr.lutfiles.lut_file
                        max_val = shelf_data_attr.lutfiles.max_val
                        legend = shelf_data_attr.lutfiles.legend
                        units = shelf_data_attr.lutfiles.units
                        shd_attribute_name = shelf_data_attr.attribute_name

                        if os.path.exists(project_root_path):
                            root, dirs, files = os.walk(project_root_path).next()
                            files.sort()

                            for f in files:
                                if f in ATTRIBUTE_CONFIG:
                                    f_path = os.path.join(project_root_path, f)
                                    fl = open(f_path)
                                    
                                    for line in fl.readlines():
                                        # print (line)
                                        line_tmp = line.split()
                                        attr_dict[line_tmp[0]] = line_tmp[1]

                        # print '!!!!!!!!!!!!!!!!!! attr_dict ======================= ', attr_dict

                        if attr_dict:
                            val_scale = attr_dict[shelf_data_attr.root_filename]
                        else:
                            val_scale = shelf_data_attr.lutfiles.val_scale

                        # val_scale = shelf_data_attr.lutfiles.val_scale

                        # print '!!!!!!!!!!!!!!!!!! val_scale ======================= ', val_scale

                        root_filename = shelf_data_attr.root_filename

                        # if data_set.is_ts:
                        #     root_filename = shelf_data_attr.root_filename
                        # else:
                        #     root_filename = shelf_data_attr.root_filename

                        shd_attribute_name = shd_attribute_name.replace(" ", "_")

                        lut_1 = '.' + lut_file.split('.')[-1]
                        lut_name = lut_file.replace(lut_1, '')

                        # print 'LUT SD ========================= ', shelf_data_attr
                        # print 'LUT UNITS ========================= ', units

                        tif_png_script = SCRIPT_TIFPNG
                        lut_file = os.path.join(LUT_DIRECTORY, lut_file)

                        max_size_command = '{0} {1}'.format(SCRIPT_MAXSIZE, file_tif)

                        if os.path.exists(file_tif):
                            out, err = Popen(max_size_command, shell=True, stdout=PIPE).communicate()
                            out = out.split('\n')

                            # print '!!!!!!!!!!!!!!!!!!!!!!! OUT ALL: ', out
                            
                            ####################### write log file
                            customer_section.write('\n\nCALC MAX SIZE: {0}\n\n'.format(out))
                            ####################### write log file

                            for n in out:
                                if 'MAX' in n:
                                    ####################### write log file
                                    customer_section.write('\n\nCALC MAX SIZE LINE MAX: {0}\n\n'.format(n))
                                    ####################### write log file
                                    line = n.split(':')
                                    max_val = line[-1].replace(' ', '')
                                    ####################### write log file
                                    customer_section.write('\n\nCALC MAX SIZE LINE MAX -1: {0}\n\n'.format(line))
                                    ####################### write log file
                                    print '!!!!!!!!!!!!!!!!!!!!!!! OUT MAX ======================= ', line[-1]

                            ####################### write log file
                            customer_section.write('\n\nCALC MAX SIZE RESULT: {0}\n\n'.format(max_val))
                            ####################### write log file

                        if shelf_data_attr.lutfiles.allow_negatives < 0:
                            max_val = max_val * -1


                        # Command Line
                        # TifPng <InpTiff> <LUTfile> [<MaxVal>] [<Legend>] [<Units>] [<ValScale>]

                        command_line = tif_png_script + ' '
                        command_line += file_tif + ' '
                        command_line += lut_file + ' '
                        command_line += str(max_val) + ' '
                        command_line += str(legend) + ' '
                        command_line += '"' + str(units) + '"' + ' '
                        command_line += str(val_scale)

                        # print '!!!!!!!!!!!!!!!!!!! LUT COMMAND NAME ========================= ', command_line
                        
                        ####################### write log file
                        customer_section.write('\n\nCOMMAND LINE: {0}\n'.format(command_line))
                        customer_section.write('\nCOMMAND LINE MAX VAL: {0}\n'.format(str(max_val)))
                        customer_section.write('\nCOMMAND LINE LEGEND: {0}\n'.format(str(legend)))
                        customer_section.write('\nCOMMAND LINE UNITS: {0}\n'.format(str(units)))
                        customer_section.write('\nCOMMAND LINE VAL SCALE: {0}\n\n'.format(str(val_scale)))
                        ####################### write log file

                        new_color_file = file_area_name + lut_name + '.png'
                        url_png = '{0}/{1}'.format(absolute_png_url, new_color_file)

                        tmp_png = file_png.split('/')[-1]
                        new_file_png = file_png.replace(tmp_png, new_color_file)

                        tmp_tif = file_tif.split('/')[-1]
                        old_file_png = file_tif.replace(tmp_tif, new_color_file)

                        legend_path_old = file_tif.split('/')[:-1]
                        legend_path_old = '/'.join(legend_path_old)

                        # print '!!!!!!!!!! LEGEND ====================== ', legend
                        # root_filename

                        if legend == '2':
                            legend_name_proj = 'FullLegend_{0}.png'.format(lut_name)
                            legend_name_map = '{0}_FullLegend_{1}.png'.format(root_filename, lut_name)
                        else:
                            legend_name_proj = 'Legend_{0}.png'.format(lut_name)
                            legend_name_map = '{0}_Legend_{1}.png'.format(root_filename, lut_name)
                            
                        old_color_legend = os.path.join(legend_path_old, legend_name_proj)
                        new_color_legend = os.path.join(LEGENDS_PATH, legend_name_map)
                        url_legend = '{0}/{1}'.format(absolute_legend_url, legend_name_map)

                        # print '!!!!!!!!! legend_name_map ================== ', legend_name_map
                        # print '!!!!!!!!! old_color_legend ================== ', old_color_legend
                        # print '!!!!!!!!! new_color_legend ================== ', new_color_legend
                        # print 'lut_name ========================= ', lut_name

                        cip_choice.png_path = new_file_png
                        cip_choice.url_png = url_png

                        cip_choice.legend_path = new_color_legend
                        cip_choice.url_legend = url_legend
                        cip_choice.save()

                        is_lutfile = True
                    else:
                        pass
                        # legend_path_old = file_tif.split('/')[:-1]
                        # legend_path_old = '/'.join(legend_path_old)
                        # legend_name = 'Legend_greyscale.png'
                        # new_legend_name = '{0}_Legend_greyscale.png'.format(customer)
                        # old_bw_legend = os.path.join(legend_path_old, legend_name)
                        # new_bw_legend = os.path.join(LEGENDS_PATH, new_legend_name)
                        # url_legend = '{0}/{1}'.format(absolute_legend_url, new_legend_name)

                        # # print '!!!!!!!!! old_bw_legend ================== ', old_bw_legend
                        # # print '!!!!!!!!! new_bw_legend ================== ', new_bw_legend

                        # cip_choice.legend_path_old = old_bw_legend
                        # cip_choice.legend_path = new_bw_legend
                        # cip_choice.url_legend = url_legend
                        # cip_choice.save()
                except AttributeError, e:
                    print '!!!!!!!!! ERROR AttributeError ================== ', e

                    # legend_path_old = file_tif.split('/')[:-1]
                    # legend_path_old = '/'.join(legend_path_old)
                    # legend_name = 'Legend_greyscale.png'
                    # new_legend_name = '{0}_Legend_greyscale.png'.format(customer)
                    # old_bw_legend = os.path.join(legend_path_old, legend_name)
                    # new_bw_legend = os.path.join(LEGENDS_PATH, new_legend_name)
                    # url_legend = '{0}/{1}'.format(absolute_legend_url, new_legend_name)

                    # print '!!!!!!!!! old_bw_legend ================== ', old_bw_legend
                    # print '!!!!!!!!! new_bw_legend ================== ', new_bw_legend

                    # cip_choice.legend_path_old = old_bw_legend
                    # cip_choice.legend_path = new_bw_legend
                    # cip_choice.url_legend = url_legend
                    # cip_choice.save()

                    warning_message = u'The LUT File is not defined! \
                                        Please specify the LUT File \
                                        for "{0}" Dataset'\
                                        .format(data_set)
                except ShelfData.DoesNotExist, e:
                    print '!!!!!!!!! ERROR ShelfData.DoesNotExist ================== ', e

                    # legend_path_old = file_tif.split('/')[:-1]
                    # legend_path_old = '/'.join(legend_path_old)
                    # legend_name = 'Legend_greyscale.png'
                    # new_legend_name = '{0}_Legend_greyscale.png'.format(customer)
                    # old_bw_legend = os.path.join(legend_path_old, legend_name)
                    # new_bw_legend = os.path.join(LEGENDS_PATH, new_legend_name)
                    # url_legend = '{0}/{1}'.format(absolute_legend_url, new_legend_name)

                    # print '!!!!!!!!! old_bw_legend ================== ', old_bw_legend
                    # print '!!!!!!!!! new_bw_legend ================== ', new_bw_legend

                    # cip_choice.legend_path_old = old_bw_legend
                    # cip_choice.legend_path = new_bw_legend
                    # cip_choice.url_legend = url_legend
                    # cip_choice.save()

                    # WARNING: NO IMAGES
                    # warning_message = u'Please specify the attribute name \
                    #                 for the Customer Info Panel "{0}".'\
                    #                 .format(cip_choice)
                        

                # Convert tif to png
                # greyscale
                
                # print '!!!!!!!!!!!!!!!!! time_series_clear ================================ ', request.session['time_series_clear']
                # print '!!!!!!!!!!!!!!!!! file_tif ================================ ', file_tif

                if not request.session['time_series_clear']:
                    try:
                        # print '!!!!!!!!!!!!!!!!! file_tif ================================ ', file_tif
                        # convert tif to png
                        if os.path.exists(file_tif):

                            # print '!!!!!!!!!!!!!!!!!!!!! is_lutfile ========================== ', is_lutfile

                            # to color
                            if is_lutfile:
                                command_line_copy_png = 'cp {0} {1}'.format(old_file_png, new_file_png)
                                command_line_copy_legend = 'cp {0} {1}'.format(old_color_legend, new_color_legend)

                                ####################### write log file
                                customer_section.write('COMMAND LINE PNG: {0}\n'.format(command_line_copy_png))
                                customer_section.write('COMMAND LINE LEGEND: {0}\n'.format(command_line_copy_legend))
                                ####################### write log file

                                # print '!!!!!!!!   COMMAND LINE =============================== 0 ', command_line
                                # print '!!!!!!!!   COMMAND LINE PNG =============================== 1 ', command_line_copy_png
                                # print '!!!!!!!!   COMMAND LINE LEGEND =============================== ', command_line_copy_legend

                                # os.environ.__setitem__('RF_TRANSPARENT', '0')
                                
                                time_convert_start = time.time()
                                time_convert_end = 0

                                # print '!!!!!!!! IS CONVERT =============================== ', is_convert_tif_png

                                if not os.path.exists(file_png) or is_convert_tif_png:
                                    # print '!!!!!!!! IS CONVERT =============================== '
                                    proc_script = Popen(command_line, shell=True)
                                    proc_script.wait()

                                    proc_script_png = Popen(command_line_copy_png, shell=True)
                                    proc_script_png.wait()

                                proc_script_legend = Popen(command_line_copy_legend, shell=True)
                                proc_script_legend.wait()

                                time_convert_end = time.time() - time_convert_start

                                print '!!!!!!!! TIME SCRIPT_TIFPNG CONVERT =============================== ', time_convert_end

                                # if not os.path.exists(new_color_legend):
                                #     command_line_copy_legend = 'cp {0} {1}'.format(old_color_legend, new_color_legend)
                                #     proc_script_legend = Popen(command_line_copy_legend, shell=True)
                                #     proc_script_legend.wait()

                                # proc_script_legend = Popen(command_line_copy_legend, shell=True)
                                # proc_script_legend.wait()

                                # subprocess.call(command_line_copy_png, shell=True)
                                # subprocess.call(command_line_copy_legend, shell=True)
                            else:
                                # command_line_copy_legend = 'cp {0} {1}'.format(old_bw_legend, new_bw_legend)
                                # 
                                # print '!!!!!!!!!!!!!!!!!!!!! file_tif ========================== ', file_tif
                                # print '!!!!!!!!!!!!!!!!!!!!! file_png ========================== ', file_png
                                # print '!!!!!!!!!!!!!!!!!!!!! 3 file_png ========================== ', file_png
                                proc = Popen(['cat', file_tif], stdout=PIPE)
                                p2 = Popen(['convert', '-', file_png], stdin=proc.stdout)
                                # subprocess.call(command_line_copy_legend, shell=True)
                        else:
                            warning_message = u'The GEO images "{0}" does not exist! \
                                                There are no attribute sub-directories defined in the "{1}" Dataset. \
                                                Please set Shelf Data for this Dataset'\
                                                .format(file_tif, data_set)


                        # print '!!!!!!!!   PNG_PATH =============================== ', PNG_PATH
                    except Exception, e:
                        print 'Popen Exception =============================== ', e

                    # get the lat/lon values for a GeoTIFF files
                    try:
                        # print '!!!!!!!!!! FILE TIF  =============================== ', file_tif

                        ds = gdal.Open(file_tif)
                        width = ds.RasterXSize
                        height = ds.RasterYSize
                        # transform = ds.GetGeoTransform()

                        # print '!!!!!!!!!!!!!!! transform =============================== ', ds.GetGeoTransform()

                        minX, Xres, Xskew, maxY, Yskew, Yres = ds.GetGeoTransform()
                        
                        maxX = minX + (ds.RasterXSize * Xres)
                        minY = maxY + (ds.RasterYSize * Yres)

                        # print '!!!!!!!!!! WIDTH =============================== ', width
                        # print '!!!!!!!!!! HIGHT =============================== ', height

                        # print '!!!!!!!!!! 1 MAX Y =============================== ', maxY
                        # print '!!!!!!!!!! 1 MAX X =============================== ', maxX

                        # print '!!!!!!!!!! 2 MIN Y =============================== ', minY
                        # print '!!!!!!!!!! 2 MIN X =============================== ', minX

                        # print '!!!!!!!!!! 2 MAX Y =============================== ', maxY
                        # print '!!!!!!!!!! 2 MAX X =============================== ', maxX
                        
                        # # ********************************************************************

                        # p= subprocess.Popen(["gdalinfo", "%s"%file_tif], stdout=subprocess.PIPE)
                        # out,err= p.communicate()
                        # ul= out[out.find("Upper Left")+15:out.find("Upper Left")+38]
                        # lr= out[out.find("Lower Right")+15:out.find("Lower Right")+38]

                        # print '!!!!!!!!!! UL  =============================== ', ul
                        # print '!!!!!!!!!! LR   =============================== ', lr
                        # print '!!!!!!!!!! GetGeoTransform =============================== ', gt
                        # print '!!!!!!!!!! width =============================== ', width
                        # print '!!!!!!!!!! height =============================== ', height
                        

                        # minx = transform[0]
                        # miny = transform[3] + (width * transform[4]) + (height * transform[5])
                        # maxx = transform[0] + (width * transform[1]) + (height * transform[2])
                        # maxy = transform[3]


                        # minY = -90.0
                        # minX = -179.9999
                        # maxY = 90.0
                        # maxX = 180.0
                        
                        # minY = -90.0
                        # minX = -179.9999
                        # maxY = 90.0
                        # maxX = 179.9999
                        
                        c_Y = request.session['center_lat']
                        c_X = request.session['center_lng']
                        
                        if (c_Y == 0.001 or c_Y == '0.001') or (c_X == 0.001 or c_X == '0.001'):
                            centerY = (maxY + minY) / 2
                            centerX = (maxX + minX) / 2
                        else:
                            centerY = c_Y
                            centerX = c_X

                        # print '!!!!!!!!!!!!!!!! ZOOM =========================== ', request.session['zoom_map']
                        # print '!!!!!!!!!!!!!!!! ZOOM google_map_zoom =========================== ', google_map_zoom
                        
                        # if cip_choice.data_set.name != 'Wheat Demo':
                        #     google_map_zoom = GOOGLE_MAP_ZOOM
                            

                        # if cip_choice.data_set.name == 'Wheat Demo':
                        if minX <= -179.9999:
                            minX = -179.9999
                            # minX = -160.0
                            # maxX = 160.0

                            # minY = -70.0
                            # maxY = 70.0

                        google_map_zoom = request.session['zoom_map']

                        # if google_map_zoom == '0.001' or google_map_zoom == 0.001:
                        #     scaleY = minY - centerY
                        #     scaleX = minX - centerX
                        #     scaleY = scaleY if scaleY >= 0 else scaleY * -1
                        #     scaleX = scaleX if scaleX >= 0 else scaleX * -1

                        #     scale = scaleY if scaleY > scaleX else scaleX

                        #     if scale >= 0.965 and scale <= 3:
                        #         google_map_zoom = 8
                        #     elif scale >= 0.6 and scale < 0.965:
                        #         google_map_zoom = 9
                        #     elif scale >= 0.435 and scale < 0.6:
                        #         google_map_zoom = 10
                        #     elif scale >= 0.17 and scale < 0.434:
                        #         google_map_zoom = 11
                        #     elif scale >= 0.095 and scale < 0.16:
                        #         google_map_zoom = 12
                        #     else:
                        #         google_map_zoom = 3


                            # print '!!!!!!!!!! SCALE Y =============================== ', scaleY
                            # print '!!!!!!!!!! SCALE X =============================== ', scaleX
                        #     print '!!!!!!!!!! SCALE =============================== ', scale
                        
                        # print '!!!!!!!!!!!!!!!! 2 ZOOM google_map_zoom =========================== ', google_map_zoom

                        # centerX = 10
                        # centerY = -10
                        
                        # minY = 30.12409
                        # minX = -85.5001
                        # maxY = 30.12599
                        # maxX = -85.4999

                        # centerY = 30.125
                        # centerX = -85.5

                        # centerY = (maxY + minY) / 2
                        # centerX = (maxX + minX) / 2
                        
                        cLng = centerX
                        cLat = centerY

                        eLat_1 = minY
                        eLng_1 = minX
                        eLat_2 = maxY
                        eLng_2 = maxX

                        if (cLat > 180 or cLat < -180) or (cLng > 180 or cLng < -180):
                            url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}\
                                    &sensor=false&language=en".format(cLat, cLng)
                            req = str(requests.get(url))

                            if '400' in req:
                                cLat = 0
                                cLng = 0

                        # print '!!!!!!!!!! E centerY =============================== ', cLat
                        # print '!!!!!!!!!! E centerX =============================== ', cLng

                        # print '!!!!!!!!!! MIN Y LAT 1 =============================== ', eLat_1
                        # print '!!!!!!!!!! MIN X LNG 1 =============================== ', eLng_1
                        # print '!!!!!!!!!! MAX Y LAT 2 =============================== ', eLat_2
                        # print '!!!!!!!!!! MAX X LNG 2 =============================== ', eLng_2

                        # print '!!!!!!!!!!!!!!!!! data_set =============================== ', cip_choice.data_set.name
                        # print '!!!!!!!!!!!!!!!!! google_map_zoom =============================== ', google_map_zoom

                    except AttributeError, e:
                        print 'GDAL AttributeError =============================== ', e
        except CustomerInfoPanel.DoesNotExist, e:
            print 'CustomerInfoPanel.DoesNotExist =============================== ', e
            warning_message = u'The file "{0}" does not exist. Perhaps the data is outdated. Please refresh the page and try again.'.format(show_file)

    customer_info_panel_show = CustomerInfoPanel.objects.filter(
                                user=customer,
                                is_show=True)

    try:
        cip_active = CustomerInfoPanel.objects.filter(
                            user=customer,
                            # data_set=data_set,
                            is_show=True)
        # file_tif_path = show_file + '.tif'
        if cip_active:
            file_tif_path = cip_active[0].tif_path

        # attribute, units = getAttributeUnits(request.user, show_file)
    except Exception:
        pass

    is_ts = False
    time_series_show = TimeSeriesResults.objects.none()
    customer_info_panel_show = CustomerInfoPanel.objects.filter(
                                user=customer, is_show=True)
    legend_scale = os.path.join(absolute_legend_url, 'Legend_greyscale.png')

    if customer_info_panel_show:
        show_dataset_cip = customer_info_panel_show[0].data_set.name
        show_image_cip = customer_info_panel_show[0].attribute_name
        show_statistic_cip = customer_info_panel_show[0].statistic
        data_set_id = customer_info_panel_show[0].data_set.id
        is_ts = customer_info_panel_show[0].data_set.is_ts
        request.session['select_data_set'] = data_set_id

        dirs_list = getResultDirectory(customer_info_panel_show[0].data_set, shelf_data_all)

        if customer_info_panel_show[0].url_legend:
            legend_scale = customer_info_panel_show[0].url_legend

        # png_name = customer_info_panel_show[0].png_path.split('/')[-1]
        # url_png = '{0}/{1}'.format(absolute_png_url, png_name)
    elif not customer_info_panel_show and data_set:
        show_dataset_cip = data_set

    # print 'show_dataset_cip ===================================== ', show_dataset_cip
    # print 'show_image_cip ===================================== ', show_image_cip
    # print 'show_statistic_cip  ===================================== ', show_statistic_cip
    # print '!!!!!!!!!!!!!!!! tab_active  ===================================== ', tab_active
    # print '!!!!!!!!!!!!!!!! time_series_list  ===================================== ', request.session['time_series_list']

    attribute_report = AttributesReport.objects.filter(user=customer)

    if attribute_report:
        for ar in attribute_report:
            if data_set.is_ts:
                show_report_ap.append(ar.attribute)
            else:
                show_report_ap.append(ar.shelfdata.attribute_name)

    ts_all = TimeSeriesResults.objects.filter(user=customer, data_set=data_set).order_by('stat_code')
    time_series_show = ts_all.order_by('result_year').distinct('result_year')
    # time_series_show = TimeSeriesResults.objects.order_by('result_year', 'stat_code').distinct(
    #                         'result_year', 'stat_code')

    # if request.session['time_series_list']:
    #     for ts in request.session['time_series_list']:
    #         time_series_list = [t.id for t in TimeSeriesResults.objects.filter(id__in=request.session['time_series_list'])] 
        # print '!!!!!!!!!!!!!!!! TS  ===================================== ', time_series_list
        # 
        # request.session['select_diagram'] = 'line'
            # request.session['select_aoi'] = 0.0001
    
    # print '!!!!!!!!!!!!!!!! SELECT AOI  ===================================== ', request.session['select_aoi']
    
    if request.session['time_series_list']:
        # print '!!!!!!!!!!!!!!!!! IF ts_selected ========================= '
        # count_1 = 0
        # count_2 = 0
        # ts_title
        # ts_subtitle
        # ts_units
        # ts_data
        # 
        #  LQ
        # Max
        # Mean
        # Median
        # Min
        # UQ
        # aoi_list = []
        ts_years = request.session['time_series_list']
        box_date = []
        box_aoi = []
        box_Min = []
        box_LQ = []
        box_Median = []
        box_UQ = []
        box_Max = []
        box_Mean = []

        # ts_selected = TimeSeriesResults.objects.filter(result_year__in=ts_years)

        ts_selected = TimeSeriesResults.objects.filter(result_year__in=ts_years, user=customer,
                                                        data_set=DataSet.objects.get(id=data_set_id)).order_by(
                                                        'customer_polygons', 'result_year', 'stat_code', 'result_date')

        time_series_list = [t.id for t in ts_selected]
        aoi_list = [n.customer_polygons for n in ts_selected]
        aoi_list = list(set(aoi_list))
        time_series_list = list(set(time_series_list))

        if request.session['select_aoi'] != 0.0001:
            aoi_ids = request.session['select_aoi']
            # aoi_ids = [241]

            # print '!!!!!!!!!!!!!!!!!!! aoi_ids ============================= ', aoi_ids

            ts_selected = ts_selected.filter(customer_polygons__in=aoi_ids).order_by(
                                                'customer_polygons', 'result_year', 'stat_code', 'result_date')

        # print '!!!!!!!!!!!!! ts_selected ======================== ', ts_selected
        # print '!!!!!!!!!!!!! AOI ======================== ', request.session['select_aoi']

        # for ts in request.session['time_series_list']:
        #     time_series_list = [t.id for t in TimeSeriesResults.objects.filter(id__in=request.session['time_series_list'])]
            

        # request.session['select_diagram']
        
        for d in ts_selected:
            # print '!!!!!!!!!!!!!!!! TS CUSTOMER ===================================== ', d.customer_polygons
            # print '!!!!!!!!!!!!!!!! TS stat_code ===================================== ', d.stat_code
            # print '!!!!!!!!!!!!!!!! TS result_year ===================================== ', d.result_year
            # print '!!!!!!!!!!!!!!!! TS result_date ===================================== ', d.result_date
            
            cur_ds = DataSet.objects.get(id=data_set_id)

            if cur_ds.name_ts:
                # print '!!!!!!!!!!!!!!!! TS NAME ===================================== ', cur_ds.name_ts
                ts_title = '"{0}"'.format(cur_ds.name_ts)
            else:
                # print '!!!!!!!!!!!!!!!! DS NAME ===================================== ', cur_ds.name
                ts_title = '"{0}" Time Series diagram'.format(cur_ds.name)



            ts_statistic = SUB_DIRECTORIES_REVERCE[d.stat_code]
            ts_units = 'Ha'

            ts_data_polygons = DataPolygons.objects.filter(
                            customer_polygons=d.customer_polygons,
                            data_set=d.data_set,
                            statistic=ts_statistic
                        )

            for tdp in ts_data_polygons:
                try:
                    ts_attribute = tdp.attribute
                    shelf_data_attr = ShelfData.objects.get(attribute_name=ts_attribute)
                    ts_units = shelf_data_attr.units
                except Exception:
                    pass

            tsr_date = str(d.result_date).split('-')

            # print '!!!!!!!!!!!!!!!! tsr_date[0] ===================================== ', tsr_date[0]
            # print '!!!!!!!!!!!!!!!! tsr_date[1] ===================================== ', tsr_date[1]
            # print '!!!!!!!!!!!!!!!! tsr_date[2] ===================================== ', tsr_date[2]
            # print '!!!!!!!!!!!!!!!! ts_series_year ===================================== ', ts_series_year

            # print '!!!!!!!!!!!!!!!! customer_polygons ===================================== ', tsr.customer_polygons
            # print '!!!!!!!!!!!!!!!! result_date ===================================== ', tsr.result_date
            
            # print '!!!!!!!!!!!!!!!! d.stat_code ===================================== ', tsr.stat_code
            # print '!!!!!!!!!!!!!!!! ts_stat_code ===================================== ', ts_stat_code
            # 
            # if tsr_date[0] != ts_series_year or ts_stat_code != d.stat_code:
                
            if request.session['select_diagram'] == 'line':
                if ts_stat_code != d.stat_code or ts_aoi_name != d.customer_polygons or ts_series_year != d.result_year:
                    # print '$$$$$$$$$$$$$$$$$$$$$$ STAT CODE ===================================== ', ts_stat_code
                    # print '$$$$$$$$$$$$$$$$$$$$$$ AOI ===================================== ', ts_aoi_name
                    ts_data = ts_data[0:-1]
                    ts_data += '$$$'
                    

                tmp = '{0},{1},{2},{3},{4},{5}$'.format(
                                d.customer_polygons.name, d.stat_code, tsr_date[0],
                                int(tsr_date[1])-1, tsr_date[2], d.value_of_time_series)
                ts_data += tmp
                ts_series_year = d.result_year
                ts_stat_code = d.stat_code
                ts_aoi_name = d.customer_polygons
                ts_result_date = d.result_date

                # print '!!!!!!!!!!!!!!!! aoi_list ===================================== ', aoi_list
                # print '!!!!!!!!!!!!!!!! tsr_data[0] ===================================== ', tsr_data[0]
                # print '!!!!!!!!!!!!!!!! ts_series_year ===================================== ', ts_series_year
                
            if request.session['select_diagram'] == 'box':
                #  LQ
                # Max
                # Mean
                # Median
                # Min
                # UQ
                # 
                # box_Min = []
                # box_LQ = []
                # box_Median = []
                # box_UQ = []
                # box_Max = []
                # box_Mean = []
                
                # box_aoi.append(str(d.customer_polygons.name))

                # if ts_result_date != d.result_date:
                #     split_date = tsr_date[2]+'/'+tsr_date[1]+'/'+tsr_date[0]
                #     box_date.append(split_date)

                    # if split_date not in box_date:
                    #     box_date.append(split_date)
                        # box_aoi.append(str(d.customer_polygons.name))
                
                if d.stat_code == 'LQ':
                    box_LQ.append(d.value_of_time_series)

                if d.stat_code == 'Max':
                    box_Max.append(d.value_of_time_series)

                if d.stat_code == 'Mean':
                    box_Mean.append(float(d.value_of_time_series))

                if d.stat_code == 'Median':
                    box_Median.append(d.value_of_time_series)

                if d.stat_code == 'Min':
                    box_aoi.append(str(d.customer_polygons.name))
                    box_Min.append(d.value_of_time_series)
                    split_date = tsr_date[2]+'/'+tsr_date[1]+'/'+tsr_date[0]
                    box_date.append(split_date)

                if d.stat_code == 'UQ':
                    box_UQ.append(d.value_of_time_series)

                # print '!!!!!!!!!!!!!!!! box_date ===================================== ', len(box_date)
                # print '!!!!!!!!!!!!!!!! box_LQ ===================================== ', len(box_LQ)
                # print '!!!!!!!!!!!!!!!! box_aoi ===================================== ', len(box_aoi)

            # ts_data += tmp
            

        # print '!!!!!!!!!!!!!!!! box_date ===================================== ', box_date
        # print '!!!!!!!!!!!!!!!! box_Max ===================================== ', box_Max

        box_aoi_name = ''
        box_year = ''
        sum_box_Mean = 0

        if request.session['select_diagram'] == 'line':
            ts_data = ts_data[0:-1]

        if request.session['select_diagram'] == 'box':
            size_box_ts = len(box_date)
            tmp_box = ''

            if box_Mean:
                sum_box_Mean = sum(box_Mean) / len(box_Mean)

            for n in xrange(size_box_ts):
                current_year = box_date[n].split('/')[2]
                if box_aoi_name != box_aoi[n] or box_year != current_year:
                    tmp_box = tmp_box[0:-1]
                    tmp_box += '$$$'
                tmp_box += box_aoi[n] + ','
                tmp_box += box_date[n] + ','
                tmp_box += str(sum_box_Mean) + ','
                tmp_box += box_Min[n] + ','
                tmp_box += box_LQ[n] + ','
                tmp_box += box_Median[n] + ','
                tmp_box += box_UQ[n] + ','
                tmp_box += box_Max[n] + '$'

                box_aoi_name = box_aoi[n]
                box_year = current_year
            
            ts_data = tmp_box[0:-1]


        for al in aoi_list:
            ts_subtitle += al.name + ', '

        ts_subtitle = ts_subtitle[0:-2]
    
    # print '!!!!!!!!!!!!!!!!! ELSE ts_selected ========================= '
    year_list = request.session['time_series_list']

    time_series_user = TimeSeriesResults.objects.filter(
                            user=customer, data_set=DataSet.objects.get(id=data_set_id)).order_by(
                                'customer_polygons', 'result_year', 'stat_code', 'result_date')

    aoi_list = [n.customer_polygons for n in time_series_user]
    aoi_list = list(set(aoi_list))
    is_delete_comma_aoi = False
    
    time_series_list = [n.id for n in TimeSeriesResults.objects.filter(
                            user=customer, data_set=DataSet.objects.get(id=data_set_id), result_year__in=year_list)]
    time_series_list = list(set(time_series_list))

    # print '!!!!!!!!!!!!!!!! year_list ===================================== ', request.session['time_series_list']
    # print '!!!!!!!!!!!!!! DataSet 1 ============================== ', DataSet.objects.get(id=data_set_id)
    # print '!!!!!!!!!!!!!! time_series_user 1 ============================== ', time_series_user
    # print '!!!!!!!!!!!!!! ts_subtitle 1 ============================== ', ts_subtitle
    
    for al in aoi_list:
        # print '!!!!!!!!!!!!!! al.name ============================== ', al.name
        if al.name not in ts_subtitle:
            ts_subtitle += al.name + ', '
            is_delete_comma_aoi = True

    if is_delete_comma_aoi:
        ts_subtitle = ts_subtitle[0:-2]

    # print '!!!!!!!!!!!!!! ts_subtitle 2 ============================== ', ts_subtitle

    ####################### write log file
    customer_section.write('\n')
    customer_section.close()

    timer_script.write('\n')
    timer_script.close()

    error_save_kml.close()
    #######################
    
    if tab_active == 'ts':
        time_series_view = True
    else:
        time_series_view = False
        request.session['time_series_clear'] = False
        time_series_list = []

    show_aoi = ''
    sub_title_aoi_select = ''

    if request.session['select_aoi'] != 0.0001:
        # for n in request.session['select_aoi']:
        #     show_aoi += n + ','

        # show_aoi = show_aoi[0:-1]
        show_aoi_select = [d.name for d in CustomerPolygons.objects.filter(id__in=request.session['select_aoi'])]
        # show_aoi_select = [d.name for d in CustomerPolygons.objects.filter(id__in=[241])]
        sub_title_aoi_select = (', ').join(show_aoi_select)

        aoi_select = ['{0}_{1}'.format(d.name, d.id) for d in CustomerPolygons.objects.filter(id__in=request.session['select_aoi'])]
        # aoi_select = ['{0}_{1}'.format(d.name, d.id) for d in CustomerPolygons.objects.filter(id__in=[241])]
        show_aoi = (',').join(aoi_select)

    if not sub_title_aoi_select and ts_subtitle:
        # sub_title_aoi_select = ts_subtitle
        sub_title_aoi_select = 'None'
        # sub_title_aoi_select = 'France'
        
    cur_ds = DataSet.objects.get(id=data_set_id)
    dirs_list_ts = []
    shelf_data_ts = cur_ds.shelf_data

    if cur_ds.name_ts:
        # print '!!!!!!!!!!!!!!!! TS NAME ===================================== ', cur_ds.name_ts
        ts_title = '"{0}"'.format(cur_ds.name_ts)
    else:
        # print '!!!!!!!!!!!!!!!! DS NAME ===================================== ', cur_ds.name
        ts_title = '"{0}" Time Series diagram'.format(cur_ds.name)

    if cur_ds.is_ts:
        dirs_list_ts = getTsResultDirectory(cur_ds)

    count_ts = request.session['count_ts']

    
    # data_sets_1 = data_sets.sort()

    # print '!!!!!!!!!!!!!!!!!! TYPE DS ========================= ', data_sets_1

    # if google_map_zoom == 0.001:
    #     google_map_zoom = 1


    # time_series_list = ''
    # ts_data = ''


    # time_series_view = request.session['time_series_view']
    
    # print '!!!!!!!!!!!!!!!! show_report_ap ===================================== ', show_report_ap
    # print '!!!!!!!!!!!!!!!! count_ts ===================================== ', count_ts
    # print '!!!!!!!!!!!!!!!! time_series_list ===================================== ', time_series_list
    # print '!!!!!!!!!!!!!!!! show_aoi_select ===================================== ', show_aoi_select
    # print '!!!!!!!!!!!!!!!! select_diagram ===================================== ', request.session['select_diagram']
    # print '!!!!!!!!!!!!!!!! ts_units ===================================== ', ts_units
    # print '!!!!!!!!!!!!!!!! ts_data ===================================== ', ts_data
    # print '!!!!!!!!!!!!!!!! ZOOM MAP ===================================== ', request.session['zoom_map']
    # print '!!!!!!!!!!!!!!!! TS VIEW SESS ===================================== ', request.session['time_series_view']
    # print '!!!!!!!!!!!!!!!! TS CLEAR ===================================== ', request.session['time_series_clear']
    # print '!!!!!!!!!!!!!!!! TS aoi_list ===================================== ', aoi_list
    # print '!!!!!!!!!!!!!!!! TS time_series_list ===================================== ', time_series_list
    
    
    data = {
        'data_sets': data_sets,
        'data_set_id': data_set_id,
        'dirs_list': dirs_list,
        'polygons': polygons,
        'attribute_list_infopanel': attribute_list_infopanel,
        'statistics_infopanel': statistics_infopanel,
        'show_dataset_cip': show_dataset_cip,
        'show_image_cip': show_image_cip,
        'show_statistic_cip': show_statistic_cip,
        'show_report_ap': show_report_ap,
        'tab_active': tab_active,
        # 'tab_active': 'aoi',
        'is_ts': is_ts,
        'time_series_show': time_series_show,
        'count_ts': count_ts,
        'dirs_list_ts': dirs_list_ts,
        'shelf_data_ts': shelf_data_ts,

        # 'time_series_list': request.session['time_series_list'],
        'time_series_list': time_series_list,
        # 'time_series_list': '',
        # 'time_series_view': request.session['time_series_view'],
        'time_series_view': time_series_view,
        'time_series_clear': request.session['time_series_clear'],
        'select_diagram': request.session['select_diagram'],
        'select_aoi': show_aoi,
        'sub_title_aoi_select': sub_title_aoi_select,

        'file_tif_path': file_tif_path,

        'warning_message': warning_message,

        'absolute_kml_url': absolute_kml_url,
        'legend_scale': legend_scale,

        'ts_title': ts_title,
        'ts_subtitle': ts_subtitle,
        'ts_units': ts_units,
        'ts_data': ts_data,
        'aoi_list': aoi_list,
        # 'aoi_list': '',
        # 'ts_series_year': ts_series_year,

        'cLng': cLng,
        'cLat': cLat,
        'eLat_1': eLat_1,
        'eLng_1': eLng_1,
        'eLat_2': eLat_2,
        'eLng_2': eLng_2,
        'GOOGLE_MAP_ZOOM': google_map_zoom,
        'absolute_url_png_file': url_png,
    }

    return data


# Delete TMP file
# @user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('customers/customer_delete_file.html')
def customer_delete_file(request):
    title = ''
    customer = request.user
    
    result_for_db = str(customer) + '_db.csv'
    db_file_path = os.path.join(TMP_PATH, result_for_db)

    ####################### write log file
    log_file = '/home/gsi/LOGS/customer_delete_file.log'
    customer_delete_f = open(log_file, 'w+')
    now = datetime.now()
    customer_delete_f.write('DATE: '+str(now))
    customer_delete_f.write('USER: {0}\n'.format(customer))
    customer_delete_f.write('DB FILE: {0}\n'.format(os.path.exists(db_file_path)))
    #######################


    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get_ajax = request.GET

        # print 'DELETES FILE data_get_ajax AJAX ============================= ', data_get_ajax
        # print 'DELETES FILE COUNT ============================= ', count_files

        if data_get_ajax.get('delete_file'):

            ####################### write log file
            customer_delete_f.write('***EXISTS db_file_path: {0} \n'.format(os.path.exists(db_file_path)))
            # customer_delete_f.write('***EXISTS result_file_path: {0} \n'.format(os.path.exists(result_file_path)))
            ####################### write log file

            
            # print '****************** EXISTS db_file_path ========================================= ', os.path.exists(db_file_path)
            # print '****************** EXISTS result_file_path ========================================= ', os.path.exists(result_file_path)


            data_set_id = int(data_get_ajax.get('delete_file'))
            data_set = DataSet.objects.get(id=data_set_id)
            # shelf_data = ShelfData.objects.all()
            is_ts = data_set.is_ts
            data_ajax = ''
            data_ajax_total = ''
            select_static = ''
            count = 0
            error = ''

            # db_file = False
            # while not db_file:

            # try:
            #     f_db = open(db_file_path)
            #     db_file = True
            # except Exception, e:
            #     # time.sleep(5)
            #     print '!!!!!!!!!! ERROR OPEN DB FILE ======================= ', e
            #     pass

            try:
                f_db = open(db_file_path)

                for l in f_db:
                    line = l.split('$$$')

                    ####################### write log file
                    customer_delete_f.write('LINE: "{0}"\n'.format(line))
                    ####################### write log file
                    
                    # print '!!!!!!!!!!!! LINE ============================= ', line

                    shd_id = line[0]
                    shelf_data = ShelfData.objects.get(id=shd_id)
                    data_ajax_total = '{0}_'.format(line[2])

                    if shelf_data.show_totals:
                        # ha = line[4].replace('\n', ' ha')
                        # ha = '{0}\n'.format(ha)
                        
                        if is_ts:
                            attr_rep = AttributesReport.objects.filter(user=customer, shelfdata=shelf_data)[count]
                            data_ajax += '{0};{1};{2};{3}'.\
                                        format(attr_rep.attribute, line[3], shelf_data.units, line[4])
                        else:
                            data_ajax += '{0};{1};{2};{3}'.\
                                        format(shelf_data.attribute_name, line[3], shelf_data.units, line[4])
                    else:
                        if is_ts:
                            attr_rep = AttributesReport.objects.filter(user=customer, shelfdata=shelf_data)[count]
                            data_ajax += '{0};{1};{2}; - \n'.\
                                        format(attr_rep.attribute, line[3], shelf_data.units)
                        else:
                            data_ajax += '{0};{1};{2}; - \n'.\
                                        format(shelf_data.attribute_name, line[3], shelf_data.units)

                    count += 1

                    ####################### write log file
                    # customer_delete_f.write('data_ajax: "{0}"\n'.format(data_ajax))
                    ####################### write log file

                data_ajax = data_ajax.replace('\n', '_')
                data_ajax_total += data_ajax[0:-1]

                # print ('!!!!!!!!!!! data_ajax ===================== '), data_ajax
                # print ('!!!!!!!!!!! data_ajax_total ===================== '), data_ajax_total

                # time.sleep(10)
                f_db.close()

                try:
                    os.remove(db_file_path)
                except Exception, e:
                    pass

                

                ####################### write log file
                # customer_delete_f.write('1 DATA AJAX EXISTS: "{0}"\n'.format(os.path.exists(ajax_file_path)))
                customer_delete_f.write('DATA AJAX END: "{0}"\n\n\n'.format(data_ajax))
                customer_delete_f.write('DATA AJAX TOTAL: "{0}"\n'.format(data_ajax_total))
                ####################### write log file

                cips = CustomerInfoPanel.objects.filter(user=customer)
                select_static = cips[0].statistic
                # data = data_ajax
                # file_for_db =

                # print 'DATA data_ajax_total ======================= ', data_ajax_total
                # print 'DATA delete_file ======================= ', delete_file
                # print 'DATA select_static ======================= ', select_static

                # return HttpResponse(data)
            except Exception:
                error = 'Please set the points to draw a AOI'

            return HttpResponse(json.dumps({'data_aoi': data_ajax_total, 'static': select_static, 'error': error}))

    data = {
        'title': title,
    }

    ####################### END write log file
    # customer_delete_f.write('1 DATA AJAX EXISTS: "{0}"\n'.format(os.path.exists(ajax_file_path)))
    customer_delete_f.close()
    #######################

    return data


def get_coord_aoi(doc):
    outer_coord = []
    inner_coord = []

    try:
        outer_boundary_is = doc.Document.Placemark.Polygon.outerBoundaryIs

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            tmp = str(doc.Document.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')
            doc_tmp_list = str(doc.Document.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)
            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp
            
            for n in doc_tmp_list:
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Document ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    line = m.split(',')
                    tmp_tuples.append(tuple(line))

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Document ========================== ', e
        pass

    try:
        outer_boundary_is = doc.Placemark.Polygon.outerBoundaryIs

        # print '!!!!!!!!!!!!!!!! TMP outer_boundary_is ======================== ', len(outer_boundary_is)

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            doc_tmp_list = str(doc.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')
            # tmp = str(doc.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            for n in doc_tmp_list:
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp
            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)

            # tmp = tmp.split(' ')

            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)
            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Placemark ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    # print '!!!!!!!!!!!!!!!!! M outer_boundary_is Placemark ========================== ', m
                    line = m.split(',')
                    tmp_tuples.append(tuple(line))

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Placemark ========================== ', e
        pass

    try:
        inner_boundary_is = doc.Document.Placemark.Polygon.innerBoundaryIs

        for n in xrange(len(inner_boundary_is)):
            tmp_tuples = []
            tmp = str(inner_boundary_is[n].LinearRing.coordinates).split('\n')

            if not tmp[0]:
                tmp = tmp[1:]

            if not tmp[-1]:
                tmp = tmp[:-1]

            for m in tmp:
                m = m.replace('\t', '')
                line = m.split(',')
                tmp_tuples.append(tuple(line))

            inner_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR inner_coord Document ========================== ', e
        pass

    try:
        inner_boundary_is = doc.Placemark.Polygon.innerBoundaryIs

        for n in xrange(len(inner_boundary_is)):
            tmp_tuples = []
            tmp = str(inner_boundary_is[n].LinearRing.coordinates).split('\n')

            if not tmp[0]:
                tmp = tmp[1:]

            if not tmp[-1]:
                tmp = tmp[:-1]

            for m in tmp:
                m = m.replace('\t', '')
                line = m.split(',')
                tmp_tuples.append(tuple(line))

            inner_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR inner_coord Placemark ========================== ', e
        pass

    # print '!!!!!!!!!!!!!!!! TMP outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!!!!!!! TMP inner_coord ======================== ', inner_coord

    return outer_coord, inner_coord


def copy_file_kml(old_path, new_path):
    error = ''
    doc = ''

    try:
        with open(old_path) as f:
            doc = parser.parse(f).getroot()

        error = validation_kml(doc, old_path)

        if error:
            if os.path.exists(old_path):
                os.remove(old_path)
            return doc, error

        command_line = 'cp {0} {1}'.format(old_path, new_path)
        proc = Popen(command_line, shell=True)
        proc.wait()
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR copy_file_kml =================== ', e
        # command_line = 'cp {0} {1}'.format(old_path, new_path)
        # proc = Popen(command_line, shell=True)
        # proc.wait()
        # error = str(e)

    return doc, error


def get_data_kml(path):
    doc = ''
    error = ''

    try:
        with open(path) as f:
            doc = parser.parse(f).getroot()
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR get_data_kml =================== ', e
        error = e

    return doc, error


def validation_kml(kml_name, kml_path):
    error_msg = ''
    file_name = kml_path.split('/')[-1]
    file_size = os.path.getsize(kml_path)
    xml = html.parse(kml_path)

    xml_extendeddata = len(xml.xpath("//extendeddata")) / 2
    xml_coordinates = len(xml.xpath("//coordinates")) / 2
    xml_point = len(xml.xpath("//point")) / 2
    xml_polygon = len(xml.xpath("//polygon")) / 2
    xml_placemark = len(xml.xpath("//placemark")) / 2

    if file_size >= 10000000:
        error_msg = 'Error!! An error occurred while loading the file "{0}". \
                    The file size is more than 10Mb'.format(file_name)
        return error_msg

    if xml_extendeddata >= 1000 or xml_coordinates >= 1000 \
        or xml_point >= 1000 or xml_polygon >= 1000 or xml_placemark >= 1000:

        error_msg = 'Error!! An error occurred while loading the file "{0}". \
                    The file has more than 1000 objects'.format(file_name)
        return error_msg

    # try:
    #     schema_ogc = Schema("ogckml22.xsd")
    #     schema_gx = Schema("kml22gx.xsd")

    #     schema_ogc.assertValid(kml_name)
    #     schema_gx.assertValid(kml_name)
    # except Exception, e:
    #     return str(e)

    return error_msg


def getUploadListTifFiles(customer, dataset, *args):
    # print '!!!!!!!!!!!!!!!!!!! args ====================== ', args
    list_files_tif = []
    # list_data_db = []
    # attributes_tmp = {}
    # attributes_reports = {}
    statistic = args[0]['statistic']
    attributes = args[0]['attr']
    upload_file = args[0]['upload_file']

    # for at in attributes:
    #     tmp = at.split('_')
    #     attributes_tmp[tmp[0]] = tmp[1]

    # for n in sorted(attributes_tmp.keys()):
    #     attributes_reports[n] = attributes_tmp[n]

    # attributes_reports = AttributesReport.objects.filter(
    #                         user=customer, data_set=dataset)
                            
    # print '!!!!!!!!!!!!!!!!!!! attributes_tmp ====================== ', attributes_tmp

    # print '!!!!!!!!!!!!!!!!!!! statistic ====================== ', statistic
    # print '!!!!!!!!!!!!!!!!!!! attributes ====================== ', attributes
    # print '!!!!!!!!!!!!!!!!!!! attributes_reports ====================== ', attributes_reports
    # print '!!!!!!!!!!!!!!!!!!! upload_file ====================== ', upload_file

    if attributes:
        if dataset.is_ts:
            # attributes_reports = attributes_reports.order_by('attribute')
            # attributes = attributes.sort()
            # attributes_reports = sorted(attributes_reports.keys())

            # print '!!!!!!!!!!!!!!!!!!! 2 attributes_reports ====================== ', attributes_reports

            for attr in attributes:
                # sub_dir = attr.shelfdata.root_filename + '/' + SUB_DIRECTORIES[attr.statistic]
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory, sub_dir)
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory)

                attr_list = attr.split('_')
                project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)

                # print '!!!!!!!!!! attr_list ========================= ', attr_list
                # print '!!!!!!!!!! sub_dir_path ========================= ', sub_dir_path
                # print '!!!!!!!!!! project_directory ========================= ', project_directory

                try:
                    if os.path.exists(project_directory):
                        pr_root, pr_dirs, pr_files = os.walk(project_directory).next()
                        pr_dirs.sort()

                        # print '!!!!!!!!!! project_directory ========================= ', project_directory
                        # print '!!!!!!!!!! attr.attribute ========================= ', attr.attribute

                        for pd in pr_dirs:
                            if pd in attr_list[0]:
                                # attribute_name = attr_list[0].split(' ')[:-1]
                                # attribute_name = str((' ').join(attribute_name))

                                # print '!!!!!!!!!! attr.attribute ========================= ', attribute_name
                                # print '!!!!!!!!!! attr.attribute TYPE ========================= ', type(attribute_name)


                                # shd_cur = ShelfData.objects.get(attribute_name=attribute_name)
                                # shd_cur = ShelfData.objects.get(attribute_name='Merchantable Volume of Timber')
                                sub_directory = os.path.join(project_directory, pd, statistic)
                                sub_root, sub_dirs, sub_files = os.walk(sub_directory).next()
                                sub_files.sort()

                                # print '!!!!!!!!!! sub_directory ========================= ', sub_directory

                                for f in sub_files:
                                    fl, ext = os.path.splitext(f)

                                    if ext == '.tif':
                                        fl_tif = os.path.join(sub_directory, f)
                                        # str_data_db = '{0}$$${1}$$$'.format(attr_list[0], fl_tif)
                                        new_fl_tif = '{0}$$${1}$$$'.format(attr_list[0], fl_tif)
                                        # str_data_db = '{0}$$${1}$$$'.format(shd_cur, fl_tif)

                                        list_files_tif.append(new_fl_tif)
                                        # list_data_db.append(str_data_db)
                                        break
                                break
                        # print '!!!!!!!!!! list_data_db ========================= ', list_data_db
                        # print '!!!!!!!!!! list_files_tif ========================= ', list_files_tif
                except Exception, e:
                    print '!!!!!!!!!! ERROR TS ========================= ', e
        else:
            # attributes_reports = attributes_reports.order_by('shelfdata__attribute_name')
            # attributes_reports = sorted(attributes_reports.keys())

            # print '!!!!!!!!!!!!!!!!!!! 2 attributes_reports ====================== ', attributes_reports

            for attr in attributes:
                attr_list = attr.split('_')
                select_shd = ShelfData.objects.get(id=attr_list[1])
                name_1 = select_shd.root_filename
                name_2 = dataset.results_directory.split('/')[0]
                tif_path = os.path.join(PROJECTS_PATH, dataset.results_directory, name_1)

                # print '!!!!!!!!!!!!!!!!!!! TIF PATH ====================== ', tif_path

                fl_tif = '{0}/{1}_{2}.{3}.tif'.format(tif_path, SUB_DIRECTORIES_REVERCE[statistic], name_1, name_2)
                new_fl_tif = '{0}$$${1}$$$'.format(select_shd.attribute_name, fl_tif)
                # str_data_db = '{0}$$${1}$$$'.format(attr_list[1], fl_tif)

                # print '!!!!!!!!!!!!!!!!!!! TIF PATH NAME ====================== ', fl_tif

                list_files_tif.append(new_fl_tif)
                # list_data_db.append(str_data_db)

    # print '!!!!!!!!!! FILE ========================= ', list_files_tif
    # print '!!!!!!!!!! DATA DB ========================= ', list_data_db

    return list_files_tif


def create_new_calculations_aoi(customer, doc_kml, data_set, *args):
    # print '!!!!!!!!!! create_new_calculations_aoi ========================= '

    info_window = ''
    attr_name = ''
    total_area = ''
    units_per_ha = ''
    total = ''
    list_value = []
    list_attr = []
    list_units = []
    list_total = []
    list_total_area = []

    list_data_kml = []

    # print '!!!!!!!!!!!!!!! ARGS  ===================== ', args

    is_ts = data_set.is_ts
    statistic = args[0]['statistic']
    attributes = args[0]['attr']
    upload_file = args[0]['upload_file']
    upload_file = upload_file.split('.kml')[0]
    count_color = get_count_color()
    outer_coord, inner_coord = get_coord_aoi(doc_kml)
    list_file_tif = getUploadListTifFiles(customer, data_set, *args)

    # print '!!!!!!!!!!!!!!! CREATE Outer Coord  ===================== ', outer_coord

    # all_coord = outer_coord + inner_coord
    kml_name ='{0} {1} AREA COORDINATE'.format(customer, data_set)

    # print '!!!!!!!!!!!!!!! ARGS  ===================== ', args
    # print '!!!!!!!!!!!!!!! outer_coord  ===================== ', len(outer_coord)
    # print '!!!!!!!!!!!!!!! all_coord  ===================== ', len(all_coord)

    # COORDINATE
    in_new_calculations_coord = str(customer) + '_in_new_calculations_coord_tmp.kml'
    out_new_calculations_coord = str(customer) + '_out_new_calculations_coord_tmp.txt'
    
    file_path_in_new_calculations_coord = os.path.join(TMP_PATH, in_new_calculations_coord)
    file_path_out_new_calculations_coord = os.path.join(TMP_PATH, out_new_calculations_coord)

    # print '!!!!!!!!!!!!!!! file_path_in_new_calculations_coord  ===================== ', file_path_in_new_calculations_coord
    # print '!!!!!!!!!!!!!!! file_path_out_new_calculations_coord  ===================== ', file_path_out_new_calculations_coord

    if os.path.exists(file_path_in_new_calculations_coord):
        os.remove(file_path_in_new_calculations_coord)

    if os.path.exists(file_path_out_new_calculations_coord):
        os.remove(file_path_out_new_calculations_coord)

    # print '!!!!!!!!!!!!!!! outer_coord  ===================== ', outer_coord[0]
    # print '!!!!!!!!!!!!!!! LEN outer_coord  ===================== ', len(outer_coord)
    
    # print '!!!!!!!!!!!!!!! list_file_tif  ===================== ', list_file_tif
    

    # if all_coord:
    for file_tif in list_file_tif:
        # *****************************************************************************
        # print '!!!!!!!!!!!!!!! outer_coord [0]  ===================== ', outer_coord[0]

        kml = simplekml.Kml()
        pol = kml.newpolygon(name=kml_name)
        pol.outerboundaryis = outer_coord[0]

        if inner_coord:
            pol.innerboundaryis = inner_coord

        kml.save(file_path_in_new_calculations_coord)

        print '!!!!!!!!!!!!!!! file_tif  ===================== ', file_tif
        
        # *****************************************************************************

        # for coord_line in all_coord:
        # kml = simplekml.Kml()
        # # kml.newpoint(name=kml_name, coords=outer_coord[0])  # lon, lat, optional height
        # kml.newpoint(name=kml_name, coords=coord_line)  # lon, lat, optional height
        # kml.save(file_path_in_new_calculations_coord)

        # *****************************************************************************

        # list_file_tif, list_data_db = getUploadListTifFiles(customer, data_set, *args)
        # list_file_tif = getUploadListTifFiles(customer, data_set, *args)
        
        # count_data = 0
        # list_val = []
        # attr_name = []
        # attr_name = ''
        # values = []


    # for file_tif in list_file_tif:
        # print '!!! FILE TIF =========================== ', file_tif

        # shd_id = list_data_db[count_data].split('$$$')[0]
        # scale = ShelfData.objects.get(id=shd_id).scale
        # command_line_ts = ''


        print '!!!!!!!!!!!!! file_tif  =========================== ', file_tif
        # print '!!!!!!!!!!!!! line_list  =========================== ', line_list

        line_list = file_tif.split('$$$')
        attr_name = line_list[0]
        shd_attr_name = attr_name

        print '!!!!!!!!!!!!! line_list  =========================== ', line_list

        if is_ts:
            shd_attr_name = attr_name.split(' ')[:-1]
            shd_attr_name = (' ').join(shd_attr_name)

        
        # print '!!!!!!!!!!!!! attr_name  =========================== ', attr_name

        units = ShelfData.objects.get(attribute_name=shd_attr_name).units

        
        # print '!!! FILE TIF  =========================== ', line_list
        # print '!!! FILE TIF 0  =========================== ', line_list[0]
        # print '!!! FILE TIF 1 =========================== ', line_list[1]

        command_line = '{0} {1} {2} {3}'.format(
                            SCRIPT_GETPOLYINFO,
                            # file_tif,
                            line_list[1],
                            file_path_in_new_calculations_coord,
                            file_path_out_new_calculations_coord
                        )

        # print '!!! COMMAND LINE =========================== ', command_line
        # print '!!! FILE =========================== ', f_tif
        proc_script = Popen(command_line, shell=True)
        proc_script.wait()

        print '!!! COMMAND LINE =========================== ', command_line

        if os.path.exists(file_path_out_new_calculations_coord):
            file_out_coord_open = open(file_path_out_new_calculations_coord)
            new_line_list = []
            

            for line in file_out_coord_open.readlines():
                new_line = line.replace(' ', '')
                new_line = new_line.replace('\n', '')
                # new_line = new_line.replace(',', '$$$')
                new_line_list.append(new_line)
                # print '!!! 1 NEW LINE LIST =========================== ', new_line_list
                # count_data += 1

            new_line_list = new_line_list[:-1]
            count_new_line_list = len(new_line_list)
            # count_line = 0
            list_val = []
            # n_val = []
            print '!!! 2 NEW LINE LIST =========================== ', new_line_list

            
            for n in new_line_list:
                nl = n.split(',')

                if len(new_line_list) > 1:
                    # nl = n.split(',')
                    # attr_name.append(nl[0])
                    # new_line[2] = '{0:,}'.format(total_aoi).replace(',', ',')
                    
                    # list_val.append(nl[1])
                    # list_val.append(nl[2])
                    # list_val.append(nl[3])
                    
                    # print '!!!!!!!!!!!!!!!!! TOTAL ======================== ', nl[1]
                    # print '!!!!!!!!!!!!!!!!! TOTAL TYPE ======================== ', type(nl[1])

                    # tot_ar = '{0:,}'.format(float(nl[1])).replace(',', ',')
                    per_ha = '{0:,}'.format(float(nl[2])).replace(',', ',')
                    tot = '{0:,}'.format(float(nl[3])).replace(',', ',')
                    
                    list_val.append(nl[1])
                    list_val.append(per_ha)
                    list_val.append(tot)
                else:
                    # total_area = nl[1]
                    # units_per_ha = nl[2]
                    # total = nl[3]
                    
                    # total_area = '{0:,}'.format(float(nl[1])).replace(',', ',')
                    total_area = nl[1]
                    units_per_ha = '{0:,}'.format(float(nl[2])).replace(',', ',')
                    total = '{0:,}'.format(float(nl[3])).replace(',', ',')

            if list_val:
                # print '!!!!!!!!!!!!!!!!! LIST VAL ======================== ', list_val

                total_area_tmp = float(list_val[0])
                units_per_ha = list_val[1]
                total = list_val[2]
                len_list_val = len(list_val)

                for n in xrange(3, len_list_val, 3):
                    # if (n+3) < len_list_val:
                    total_area_tmp -= float(list_val[n])

                    # print '!!!!!!!!!!!!!!! list_val[n+3] =========================== ', list_val[n]

                # total_area = str(total_area_tmp)
                total_area = '{0:,}'.format(total_area_tmp).replace(',', ',')
                total_area_tmp = 0

            # print '!!!!!!!!!!!!!!! attr_name =========================== ', attr_name
            # print '!!!!!!!!!!!!!!! total_area =========================== ', total_area
            # print '!!!!!!!!!!!!!!! units_per_ha =========================== ', units_per_ha
            # print '!!!!!!!!!!!!!!! total =========================== ', total
            # print '!!!!!!!!!!!!! LIST VAL =========================== ', list_val
            # print '!!!!!!!!!!!!! ATTR NAME =========================== ', attr_name
            
            list_attr.append(attr_name)
            list_units.append(units)
            list_value.append(units_per_ha)
            list_total.append(total)
            list_total_area.append(total_area)

        tmp_info_window = '<tr>';
        tmp_info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attr_name)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(units_per_ha)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(units)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(total)
        tmp_info_window += '</tr>\n'
        list_data_kml.append(tmp_info_window)

        # print '!!! total_area =========================== ', total_area
        # print '!!! units_per_ha =========================== ', units_per_ha
        # print '!!! total =========================== ', total
    print '!!!!!!!!!!!!!!!!!!! list_data_kml =========================== ', list_data_kml


    # try:
    #     try:
    #         name_kml = doc_kml.Document.Placemark.description
    #     except Exception, e:
    #         name_kml = doc_kml.Document.Placemark.name
    # except Exception:
    #     name_kml = ''

    info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(
                                                COLOR_HEX_NAME[count_color], upload_file)
    info_window += '<p align="center"><span><b>Total Area:</b></span> {0} ha</p>'.format(total_area)
    info_window += '<p align="center"><span><b>Values:</b></span> {0}</p>'.format(SUB_DIRECTORIES_REVERCE[statistic])
    info_window += '<div style="overflow:auto;" class="ui-widget-content">'

    info_window += '<table border="1" cellspacing="5" cellpadding="5" style="border-collapse:collapse;border:1px solid black;width:100%;">\n'
    info_window += '<thead>\n'
    info_window += '<tr bgcolor="#CFCFCF">\n'
    info_window += '<th align="left" style="padding:10px">Attribute</th>\n'
    info_window += '<th style="padding:10px">Units per Hectare</th>\n'
    info_window += '<th style="padding:10px">Units</th>\n'
    info_window += '<th style="padding:10px">Total</th>\n'
    info_window += '</tr>\n'
    info_window += '</thead>\n'
    info_window += '<tbody>\n'

    # print '!!!!!!!!!!!!!!!!!!!!!!!! list_data_kml ================================= ', list_data_kml

    for n in xrange(len(list_data_kml)):
        if n % 2 == 0:
            info_window += '<tr bgcolor="#F5F5F5">\n'
        else:
            info_window += '<tr>';

        info_window += list_data_kml[n]
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(list_value[n])



        # info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attribute[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(value[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(units[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(total[n])

        # info_window += '</tr>\n'

    info_window += '</tbody>\n'
    info_window += '</table>\n'
    info_window += '</div>'

    # print '!!!!!!!!!!!! info_window =========================== ', info_window

    return info_window, list_attr, list_units, list_value, list_total, list_total_area


# Lister files
@login_required
@render_to('customers/files_lister.html')
def files_lister(request):
    customer = request.user
    calculation_aoi = False
    upload_file = ''
    count_color = get_count_color()
    data_set = DataSet.objects.none()
    shelf_data_all = ShelfData.objects.all().order_by('attribute_name')
    path_ftp_user = os.path.join(FTP_PATH, customer.username)
    path_kml_user = os.path.join(KML_PATH, customer.username)
    dir_kml_user = os.path.join(KML_DIRECTORY, customer.username)
    # files_list = os.listdir(path_ftp_user)
    url_path = os.path.join('/media/CUSTOMER_FTP_AREA', customer.username)

    # The url to are PNG, KML urls
    scheme = '{0}://'.format(request.scheme)
    absolute_kml_url = os.path.join(scheme, request.get_host(), KML_DIRECTORY, customer.username)

    cip_ds = CustomerInfoPanel.objects.filter(user=customer)

    if cip_ds:
        data_set = cip_ds[0].data_set

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post_ajax = request.POST

        # print '!!!!!!!!!!! AJAX POST ====================== ', data_post_ajax

        if 'cur_run_id' in data_post_ajax:
            message = u'Are you sure you want to remove this objects:'
            file_customer = data_post_ajax['cur_run_id']
            data = '<b>"' + file_customer + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    if request.method == "POST":
        data_post = request.POST
        form = UploadFileForm(request.POST, request.FILES)

        # print '!!!!!!!!!! POST ================== ', data_post
        # print '!!!!!!!!!!!!! DATA SET ==================== ', request.session['select_data_set']
        
        if 'load_button' in data_post:
            if form.is_valid():
                info_window = ''
                name_kml = ''
                file_name = str(request.FILES['test_data']).decode('utf-8')
                path_test_data = os.path.join(path_ftp_user, file_name)

                # print '!!!!!!!!!! FILE NAME ================== ', file_name

                if not os.path.exists(path_ftp_user):
                    os.makedirs(path_ftp_user)

                if not os.path.exists(path_kml_user):
                    os.makedirs(path_kml_user)

                if os.path.exists(path_test_data):
                    os.remove(path_test_data)


                # print '!!!!!!!!!! path_kml_user ================== ', path_kml_user

                f_name = str(file_name).split('.')[:-1]
                ext = str(file_name).split('.')[-1]

                # print '!!!!!!!!!! FILE NAME ================== ', f_name
                # print '!!!!!!!!!! FILE EXT ================== ', ext

                handle_uploaded_file(request.FILES['test_data'],
                                     path_test_data)

                if ext == 'kml':
                    kml_url = os.path.join(absolute_kml_url, file_name)
                    new_path = os.path.join(path_kml_user, file_name)
                    doc_kml, error = copy_file_kml(path_test_data, new_path)

                    if error:
                        # print '!!!!!!!!!!!!!!! ERROR  ===================== ', error
                        # os.mkdir()

                        return HttpResponseRedirect(u'%s?warning_message=%s' % (
                                reverse('files_lister'),
                                (u'{0}'.format(error))))

                    try:
                        if not error:
                            count_color = get_count_color()
                            upload_file = file_name

                            try:
                                if doc_kml.Document.Placemark.Polygon.outerBoundaryIs:
                                    calculation_aoi = True
                            except Exception, e:
                                print '!!!!!!!!!!!!!!! ERROR KML Document  ===================== ', e

                            try:
                                if doc_kml.Placemark.Polygon.outerBoundaryIs:
                                    calculation_aoi = True
                            except Exception, e:
                                print '!!!!!!!!!!!!!!! ERROR KML Placemark  ===================== ', e

                            info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(
                                                COLOR_HEX_NAME[count_color], f_name)

                    except Exception, e:
                        print '!!!!!!!!!!!!!!! ERROR COPY KML ===================== ', e
                        pass

                    # print '!!!!!!!!!!!! COORDINATE ======================== ', doc_kml.Document.Polygon.outerBoundaryIs.LinearRing.coordinates

                    load_aoi = addPolygonToDB(
                                    f_name[0], file_name, customer,
                                    new_path, kml_url,
                                    data_set, text_kml=info_window
                                )

        if 'delete_button' in data_post:
            filename_customer = data_post['delete_button']
            path_filename_ftp = os.path.join(path_ftp_user, filename_customer)
            # path_filename_kml = os.path.join(KML_PATH, filename_customer)
            path_filename_kml = os.path.join(KML_PATH, customer.username, filename_customer)

            try:
                os.remove(path_filename_ftp)
                
                if os.path.exists(path_filename_kml):
                    os.remove(path_filename_kml)
                    CustomerPolygons.objects.filter(kml_path=path_filename_kml).delete()
            except Exception, e:
                print '!!!!! ERROR FTP KML FILE ================ ', e

        if 'calculate-data' in data_post:
            # print '!!!!!!!!!! POST ================== ', data_post
            # print '!!!!!!!!!! POST LIST ================== ', data_post.lists()

            try:
                upload_fl = ''
                select_stat = ''
                error = ''
                select_attr = []
                upload_data = data_post.lists()

                for item in upload_data:
                    # print '!!!!!!!!!! item 0 ================== ', item[0]
                    # print '!!!!!!!!!! item 1 ================== ', item[1]

                    if 'upload-file' in item:
                        upload_fl = item[1][0]

                    if 'select-statistic' in item:
                        select_stat = item[1][0]

                    if 'select-attr' in item:
                        select_attr = item[1]

                        # for n in tmp_list:
                        #     select_attr.append(n.split('_')[1])

                if upload_fl:
                    path_test_data = os.path.join(path_ftp_user, upload_fl)
                    # new_path = os.path.join(KML_PATH, upload_fl)
                    new_path = os.path.join(KML_PATH, customer.username, upload_fl)


                    doc_kml, error = get_data_kml(new_path)


                    print '!!!!!!!!!!!!!!!! ERROR KML ============================ ', error

                if not error and upload_fl:
                    data_args = {
                        'upload_file': upload_fl,
                        'statistic': select_stat,
                        'attr': select_attr
                    }

                    new_info_window, list_attr, list_units, list_value, list_total, list_total_area = create_new_calculations_aoi(
                                            customer, doc_kml, data_set, data_args
                                        )

                    print '!!!!!!!!!! new_info_window ================== ', new_info_window

                    area_name = upload_fl.split('.kml')[0]
                    outer_coord, inner_coord = get_coord_aoi(doc_kml)
                    data_coord = {
                        'outer_coord': outer_coord,
                        'inner_coord': inner_coord
                    }

                    print '!!!!!!!!!! COORD outer_coord ================== ', outer_coord
                    print '!!!!!!!!!! COORD inner_coord ================== ', inner_coord
                    # print '!!!!!!!!!! DATA COORD ================== ', data_coord

                    cur_polygon = createKml(customer, area_name, new_info_window,
                                            absolute_kml_url, data_set, count_color, data_coord)
                    len_attr = len(select_attr)

                    for n in xrange(len_attr):
                        if not DataPolygons.objects.filter(user=customer, data_set=data_set,
                            customer_polygons=cur_polygon, attribute=select_attr[n]).exists():
                                DataPolygons.objects.create(
                                    user=request.user,
                                    customer_polygons=cur_polygon,
                                    data_set=data_set,
                                    attribute=list_attr[n],
                                    statistic=select_stat,
                                    value=list_value[n],
                                    units=list_units[n],
                                    total=list_total[n],
                                    total_area=list_total_area[n]+' ha'
                                )
                        elif DataPolygons.objects.filter(user=request.user, data_set=data_set,
                            customer_polygons=cur_polygon, attribute=select_attr[n]).exists():
                                DataPolygons.objects.filter(user=request.user, data_set=data_set,
                                    customer_polygons=cur_polygon, attribute=select_attr[n]
                                ).update(
                                    # attribute=attribute[n],
                                    statistic=select_stat,
                                    value=list_value[n],
                                    units=list_units[n],
                                    total=list_total[n],
                                    total_area=list_total_area[n]+' ha'
                                )

                    path_kml = os.path.join(KML_PATH, customer.username, upload_fl)
                    command_line_copy_kml = 'cp {0} {1}'.format(path_kml, path_ftp_user)
                    proc_copy_kml = Popen(command_line_copy_kml, shell=True)
                    proc_copy_kml.wait()

                    # if data_set.is_ts:
                    #     createTimeSeriesResults(cur_polygon, file_path_in_coord_tmp,
                    #                             file_path_out_ts_coord_tmp)

                
                # print '!!!!!!!!!! result_load_kml ================== ', result_load_kml
                # print '!!!!!!!!!! FILE ================== ', upload_fl
                # print '!!!!!!!!!! FILE PATH ================== ', path_test_data
                # print '!!!!!!!!!! FILE NEW PATH ================== ', new_path
                # print '!!!!!!!!!! STAT ================== ', select_stat
                # print '!!!!!!!!!! ATTR ================== ', select_attr
            except Exception, e:
                print '!!!!!!!!!!!!!!!! ERROR UPLOAD FILE NAME ========================== ', e


    else:
        form = UploadFileForm()

    if data_set:
        if data_set.is_ts:
            dirs_list = getTsResultDirectory(data_set)
        else:
            dirs_list = getResultDirectory(data_set, shelf_data_all)
    

    dirs, files, info_message = get_files_dirs(url_path, path_ftp_user)

    # print '!!!!!!!!!!!!!!!!!!!! FILES LIST ================================ ', files
    # print '!!!!!!!!!!!!!!!!!!!! IS CALCULATIONS ================================ ', calculation_aoi

    data = {
        'data_set': data_set,
        'dirs_list': dirs_list,
        'files': files,
        'form': form,
        'calculation_aoi': calculation_aoi,
        'upload_file': upload_file
    }

    return data
