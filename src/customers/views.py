# -*- coding: utf-8 -*-
"""Views for the customers app."""
import os, numpy
import os.path, time
import subprocess
from PIL import Image
from subprocess import check_call, Popen, PIPE
from osgeo import osr, gdal
import simplekml
import pickle

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

from customers.models import (Category, ShelfData, DataSet, CustomerAccess,
                                CustomerInfoPanel, CustomerPolygons)
from customers.customers_forms import (CategoryForm, ShelfDataForm, DataSetForm,
                                        CustomerAccessForm, CustomerPolygonsForm)
from customers.customers_update_create import (category_update_create, shelf_data_update_create,
                                                data_set_update_create, customer_access_update_create)
from core.get_post import get_post
from core.paginations import paginations
from gsi.settings import (BASE_DIR, RESULTS_DIRECTORY, GOOGLE_MAP_ZOOM, POLYGONS_DIRECTORY, MEDIA_ROOT, TMP_PATH,
                        DAFAULT_LAT, DAFAULT_LON, PNG_DIRECTORY, PNG_PATH, PROJECTS_PATH, KML_DIRECTORY, KML_PATH)


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

    categorys = Category.objects.all()
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
        'available_tiles': available_tiles,
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

    shelf_data = ShelfData.objects.all()
    shelf_data_name = ''

    # Sorted
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('category', 'attribute_name', 'root_filename', 'units',):
            shelf_data = shelf_data.order_by(order_by)

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
                reverse('shelf_data_list'),
                (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        elif request.POST.get('delete_button'):
            cur_shelf_data = get_object_or_404(ShelfData, pk=request.POST.get('delete_button'))
            shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
            cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data_list'), (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('shelf_data_list'), (u"To delete, select Shelf Data or more Shelf Data.")))

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
    title = 'Category Edit "%s"' % (shelf_data.attribute_name)
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

    data_sets = DataSet.objects.all()
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
                        results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']
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
        results_directory = RESULTS_DIRECTORY + data_set.results_directory
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
                    results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']

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

    customers_access = CustomerAccess.objects.all()
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
                customer_access_name += '"{0}", '.format(cur_customer_access)
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


def remove_file_png(file_path):
    # Get the png file for the delete
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception, e:
        print 'Exception remove file png ========================= ', e


def check_current_dataset(request, data_post):
    data_set_id = data_post.get('datasets_id', '')
    request.session['select_data_set'] = data_set_id
    data_set = DataSet.objects.get(pk=data_set_id)

    # print 'data_set_id ==================================', data_set_id

    if not CustomerInfoPanel.objects.filter(user=request.user, data_set=data_set).exists():
        info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()


def check_date_files(file_tif, file_png):
    try:
        f_tif = os.path.getmtime(file_tif)
        f_png = os.path.getmtime(file_png)

        if f_tif > f_png:
            return True
    except Exception, e:
        print 'Exception check_date_files ========================= ', e
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
    
    
def addPolygonToDB(name, kml_name, user, kml_path):
    if CustomerPolygons.objects.filter(name=name).exists():
        CustomerPolygons.objects.filter(name=name).update(
            name=name,
            kml_name=kml_name,
            user=user,
            kml_path=kml_path
        )
    else:
        customer_pol = CustomerPolygons.objects.create(
                            name=name,
                            kml_name=kml_name,
                            user=user,
                            kml_path=kml_path
                        )
    
    
def createKml(user, filename, info_window):
    # Create KML file for the draw polygon
    kml_filename = str(filename) + '.kml'
    tmp_file = str(user) + '_coord_tmp.txt'
    tmp_path = os.path.join(KML_PATH, tmp_file)
    coord = getGeoCoord(tmp_path)
    
    # print 'coord ========================== ', coord
    
    kml = simplekml.Kml()
    pol = kml.newpolygon(name=filename)
    pol.outerboundaryis.coords = coord
    pol.style.linestyle.color = simplekml.Color.hex('#ffffff')
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.hex('#8bc53f'))
    
    pol.style.balloonstyle.text = info_window
    pol.style.balloonstyle.bgcolor = simplekml.Color.lightgreen
    pol.style.balloonstyle.textcolor = simplekml.Color.hex('#283890')

    kml_path = os.path.join(KML_PATH, kml_filename)
    kml.save(kml_path)
    
    addPolygonToDB(filename, kml_filename, user, kml_path)
    
    
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


# view Customer Section
@login_required
@render_to('customers/customer_section.html')
def customer_section(request):
    """**View for the "Customer '<user>' section" page.**

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
    
    customer = request.user
    shelf_data_all = ShelfData.objects.all()
    customer_info_panel = CustomerInfoPanel.objects.filter(user=request.user)
    customer_polygons = CustomerPolygons.objects.filter(user=request.user)
    
    title = 'Customer {0} section'.format(customer)
    url_name = 'customer_section'
    polygons_path = os.path.join(MEDIA_ROOT, 'kml')
    warning_message = ''
    select_area = None

    project_directory = ''
    info_panel = None
    data_set = None
    data_sets = []
    dirs_list = []
    dirs_infopanel = []
    files_infopanel = []
    statisctics_infopanel = []
    polygons = []
    data_set_id = 0
    show_file = ''
    file_tif = ''
    # polygon = ''
    # coord = []
    name_dataset = ''
    attribute = ''
    units = ''
    file_tif_path = ''
    show_totals = ''
    
    php_query = False
    
    # default GEOTIFF coordinates
    cLng = DAFAULT_LON
    cLat = DAFAULT_LAT
    eLat_1 = 0
    eLng_1 = 0
    eLat_2 = 0
    eLng_2 = 0
    google_map_zoom = 6
    url_png = ''
    
    # The path to are PNG and KML folders
    scheme = '{0}://'.format(request.scheme)
    absolute_png_url = os.path.join(scheme, request.get_host(), PNG_DIRECTORY)
    absolute_kml_url = os.path.join(scheme, request.get_host(), KML_DIRECTORY)
    
    # request.session['file_info_panel'] = ''

    # Get the User DataSets
    try:
        customer_access = CustomerAccess.objects.get(user=customer)
        data_sets_current = CustomerAccess.data_set.through.objects.filter(
                        customeraccess_id=customer_access.id).order_by('dataset_id')

        for n in data_sets_current:
            try:
                ds = DataSet.objects.get(pk=n.dataset_id)
                data_sets.append(ds)
            except Exception:
                pass
    except Exception, e:
        print 'ERROR ==================== ', e
        error_message = 'You have no one DataSet for view. Please contact to the admin.'
        data = {
            'title': title,
            'customer': customer,
            'url_name': url_name,
            'error_message': error_message
        }

        return data

    # Get select data_set sessions
    if request.session.get('select_area', False):
        select_area = request.session['select_area']
        select_area = int(select_area)
    else:
        request.session['select_area'] = 0
    
    if request.session.get('select_data_set', False):
        data_set_id = request.session['select_data_set']
        data_set_id = int(data_set_id)
    else:
        CustomerInfoPanel.objects.filter(user=request.user).delete()
        if data_sets:
            request.session['select_data_set'] = data_sets[0].id
        else:
            if customer_info_panel:
                request.session['select_data_set'] = customer_info_panel[0].data_set.id
            else:
                request.session['select_data_set'] = data_set_id
        # request.session.set_expiry(172800)
        
    name_dataset = get_object_or_404(DataSet, id=int(request.session['select_data_set'])).name
    
    # Get select image area sessions
    if request.session.get('file_info_panel', False):
        show_file = request.session['file_info_panel']
    else:
        if customer_info_panel:
            request.session['file_info_panel'] = customer_info_panel[0].file_area_name
            show_file = request.session['file_info_panel']
        else:
            request.session['file_info_panel'] = show_file
        # request.session.set_expiry(172800)

    # get AJAX POST for KML files
    if request.is_ajax() and request.method == "POST":
        data_post_ajax = request.POST
        
        # print 'data_post_ajax ===================== ', data_post_ajax
    
        if 'send_data[0][]' in data_post_ajax:
            coord_tmp = str(request.user) + '_coord_tmp.txt'
            php_tmp = str(request.user) + '_php_tmp.txt'
            file_path_coord = os.path.join(KML_PATH, coord_tmp)
            file_path_php = os.path.join(KML_PATH, php_tmp)
            myfile_coord = open(file_path_coord, "w")
            myfile_php = open(file_path_php, "w")
            
            list_size = len(data_post_ajax.lists()) - 1
            coord = []*list_size
            tmp = {}
            coord_dict = {}
            lon = []
            lat = []
            
            for n in data_post_ajax.lists():
                if n[0] != 'csrfmiddlewaretoken':
                    index = getIndex(n[0])
                    tmp[index] = n[1]

            for k in sorted(tmp.keys()):
                coord_dict[k] = tmp[k]
                
            for n in coord_dict:
                myfile_coord.write(",".join(coord_dict[n]));
                myfile_coord.write("\n");
                
            for n in coord_dict:
                lon.append(coord_dict[n][0])
                lat.append(coord_dict[n][1])
                
            lat_str = ','.join(lat)
            lon_str = ','.join(lon)
            
            myfile_php.write(lat_str);
            myfile_php.write("\n");
            myfile_php.write(lon_str);
            myfile_php.write("\n");
            
            myfile_coord.close()
            myfile_php.close()
            
            # print 'coord_dict ======================== ', coord_dict
            
            status = 'success'

            return HttpResponse(status)
            
        if 'cur_run_id' in data_post_ajax:
            message = u'Are you sure you want to remove this objects:'
            arrea = data_post_ajax['cur_run_id']
            data = u'Are you sure you want to remove this objects: <b>"{0}"</b>?'.format(arrea)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)
        
    # get AJAX GET
    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get = request.GET
        cip = CustomerInfoPanel.objects.filter(user=request.user)
        
        print 'GET customer_section ====================== ', data_get
        
        # When user celect a new DataSet, the previous celected DataSet to remove
        if 'datasets_id' in data_get:
            for ip in cip:
                remove_file_png(ip.png_path)

            check_current_dataset(request, data_get)

        if 'remove_all_selected_items' in data_get:
            request.session['file_info_panel'] = ''
            for ip in cip:
                remove_file_png(ip.png_path)

            CustomerInfoPanel.objects.filter(user=request.user).delete()

        if 'show_file_arrea' in data_get:
            request.session['file_info_panel'] = data_get.get('show_file_arrea', '')
            
        if 'polygon' in data_get:
            # for ip in cip:
            #     remove_file_png(ip.png_path)
            #
            # CustomerInfoPanel.objects.filter(user=request.user).delete()
            
            polygon = data_get.get('polygon', '')
            data = os.path.join(absolute_kml_url, polygon)
            
        if 'cur_area' in data_get:
            request.session['select_area'] = data_get.get('cur_area', '')
            select_area = get_object_or_404(CustomerPolygons, pk=request.session['select_area'])
            data = select_area.name
            
        status = 'success'

        return HttpResponse(data)

    # Get data for the Info Panel
    try:
        data_set = DataSet.objects.get(pk=data_set_id)
    except Exception, e:
        print 'Exception 01 ========================= ', e
        # print 'Exception 01 data_set ========================= ', request.session['select_data_set']
        if data_sets:
            data_set = data_sets[0]
            data_set_id = int(data_set.id)

    # Get the results_directory list
    try:
        project_directory = os.path.join(PROJECTS_PATH, data_set.results_directory)
        root, dirs, files = os.walk(project_directory).next()

        for sd in shelf_data_all:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)
    except Exception, e:
        print 'Exception 02 ========================= ', e
        warning_message = u'The directory "{0}" does not exist!'.format(project_directory)
        # error = True
        # return HttpResponseRedirect(
        #     u'%s?danger_message=%s' % (reverse('customer_section'),
        #     (u'The directory "{0}" does not exist!'.format(project_directory)))
        # )
    
    # Handling POST request
    if request.method == "POST":
        data_post = request.POST
        form = CustomerPolygonsForm(request.POST)
        dirs = []
        
        # print 'POST ============================= ', data_post
        
        if request.POST.get('delete_button'):
            kml_file = data_post.get('delete_button')
            cur_area = get_object_or_404(
                CustomerPolygons, kml_name=kml_file)
            os.remove(cur_area.kml_path)
            cur_area.delete()
        
            return HttpResponseRedirect(u'%s' % (reverse('customer_section')))
                    
        if request.POST.get('area_name', ''):
            area_id = request.session['select_area']
            
            if area_id:
                old_area = CustomerPolygons.objects.get(pk=area_id)
                new_area_name = data_post.get('area_name')
                new_area_name = new_area_name.replace(' ', '-')
                new_kml_name = str(new_area_name) + '.kml'
                old_path = old_area.kml_path
                new_path = os.path.join(KML_PATH, new_kml_name)
                
                os.rename(old_path, new_path)
                
                area = CustomerPolygons.objects.filter(pk=area_id).update(
                            name = new_area_name,
                            kml_name = new_kml_name,
                            kml_path = new_path)
                
                return HttpResponseRedirect(u'%s' % (reverse('customer_section')))
        
        if 'save_area' in data_post:
            area_name = data_post.get('file_name', '')
            total_area = data_post.get('total_area', '')
            
            tree_count = data_post.get('tree_count', '')
            area_name = area_name.replace(' ', '-')
            attribute, units = getAttributeUnits(request.user, show_file)
            
            shelf_dt = ShelfData.objects.get(attribute_name=attribute, units=units)
            show_totals = shelf_dt.show_totals
            
            info_window = '''
            <p><b>Area "{0}"</b></p>
            <p>Total Area: {1} ha</p>
            <p>{2}: {3} {4}</p>
            '''.format(area_name, total_area, attribute, tree_count, units)
            
            if show_totals and data_post.get('count_hectare', ''):
                count_hectare = data_post.get('count_hectare', '')
                info_window += '''
                <p>Area total: {0} {1}</p>
                '''.format(count_hectare, units)
            
            # Create KML file for the draw polygon
            createKml(request.user, area_name, info_window)
        
        if 'add-list-view' in data_post:
            if 'root_filenames[]' in data_post and 'statistics[]' in data_post:
                info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
                dirs = data_post.getlist('root_filenames[]')
                statistics = data_post.getlist('statistics[]')
                data_set = DataSet.objects.get(pk=data_set_id)
                results_directory = data_set.results_directory
                project_name = results_directory.split('/')[0]

                for dr in dirs:
                    shelf_data = ShelfData.objects.get(pk=dr)
                    attribute_name = shelf_data.attribute_name

                    for st in statistics:
                        file_area_name = '{0}_{1}.{2}'.format(st, shelf_data.root_filename, project_name)
                        tif = '{0}.tif'.format(file_area_name)
                        png = '{0}.png'.format(file_area_name)
                        tif_path = os.path.join(PROJECTS_PATH, data_set.results_directory, shelf_data.root_filename, tif)
                        png_path = os.path.join(PNG_PATH, png)
                        url_png = '{0}/{1}'.format(absolute_png_url, png)
                        info_panel = CustomerInfoPanel.objects.create(
                                        user=request.user,
                                        data_set=data_set,
                                        attribute_name=attribute_name,
                                        statisctic=st,
                                        file_area_name=file_area_name,
                                        tif_path=tif_path,
                                        png_path=png_path,
                                        url_png=url_png)
                        info_panel.save()
            elif 'root_filenames[]' in data_post and not 'statistics[]' in data_post:
                info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
                dirs = data_post.getlist('root_filenames[]')

                data_set = DataSet.objects.get(pk=data_set_id)
                results_directory = data_set.results_directory
                project_name = results_directory.split('/')[0]

                for dr in dirs:
                    shelf_data = ShelfData.objects.get(pk=dr)
                    attribute_name = shelf_data.attribute_name

                    for st in ATTRIBUTE_NAMES:
                        file_area_name = '{0}_{1}.{2}'.format(st, shelf_data.root_filename, project_name)
                        tif = '{0}.tif'.format(file_area_name)
                        png = '{0}.png'.format(file_area_name)
                        tif_path = os.path.join(PROJECTS_PATH, data_set.results_directory, shelf_data.root_filename, tif)
                        png_path = os.path.join(PNG_PATH, png)
                        url_png = '{0}/{1}'.format(absolute_png_url, png)
                        info_panel = CustomerInfoPanel.objects.create(
                                        user=request.user,
                                        data_set=data_set,
                                        attribute_name=attribute_name,
                                        statisctic=st,
                                        file_area_name=file_area_name,
                                        tif_path=tif_path,
                                        png_path=png_path,
                                        url_png=url_png)
                        info_panel.save()
            elif not 'root_filenames[]' in data_post and 'statistics[]' in data_post:
                info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
                statistics = data_post.getlist('statistics[]')
                data_set = DataSet.objects.get(pk=data_set_id)
                results_directory = data_set.results_directory
                project_name = results_directory.split('/')[0]

                for dr in dirs_list:
                    attribute_name = dr.attribute_name

                    for st in statistics:
                        file_area_name = '{0}_{1}.{2}'.format(st, dr.root_filename, project_name)
                        tif = '{0}.tif'.format(file_area_name)
                        png = '{0}.png'.format(file_area_name)
                        tif_path = os.path.join(PROJECTS_PATH, data_set.results_directory, dr.root_filename, tif)
                        png_path = os.path.join(PNG_PATH, png)
                        url_png = '{0}/{1}'.format(absolute_png_url, png)
                        info_panel = CustomerInfoPanel.objects.create(
                                        user=request.user,
                                        data_set=data_set,
                                        attribute_name=attribute_name,
                                        statisctic=st,
                                        file_area_name=file_area_name,
                                        tif_path=tif_path,
                                        png_path=png_path,
                                        url_png=url_png)
                        info_panel.save()
            elif not 'root_filenames[]' in data_post and not 'statistics[]' in data_post:
                info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
                data_set = DataSet.objects.get(pk=data_set_id)
                results_directory = data_set.results_directory
                project_name = results_directory.split('/')[0]

                for dr in dirs_list:
                    attribute_name = dr.attribute_name

                    for st in ATTRIBUTE_NAMES:
                        file_area_name = '{0}_{1}.{2}'.format(st, dr.root_filename, project_name)
                        tif = '{0}.tif'.format(file_area_name)
                        png = '{0}.png'.format(file_area_name)
                        tif_path = os.path.join(PROJECTS_PATH, data_set.results_directory, dr.root_filename, tif)
                        png_path = os.path.join(PNG_PATH, png)
                        url_png = '{0}/{1}'.format(absolute_png_url, png)
                        info_panel = CustomerInfoPanel.objects.create(
                                        user=request.user,
                                        data_set=data_set,
                                        attribute_name=attribute_name,
                                        statisctic=st,
                                        file_area_name=file_area_name,
                                        tif_path=tif_path,
                                        png_path=png_path,
                                        url_png=url_png)
                        info_panel.save()

            if CustomerInfoPanel.objects.filter(user=request.user).exists():
                try:
                    customer_info_panel = CustomerInfoPanel.objects.filter(user=request.user)
                    request.session['file_info_panel'] = customer_info_panel[0].file_area_name
                    show_file = customer_info_panel[0].file_area_name
                except Exception, e:
                    print 'CustomerInfoPanel Exception ======================== ', e
                    pass
                    
    # Get selected data for the InfoPanel display
    if data_set:
        customer_info_panel = CustomerInfoPanel.objects.filter(user=request.user)

        if customer_info_panel:
            file_area = customer_info_panel.values_list('file_area_name', flat=True)
            attribute_name = customer_info_panel.values_list('attribute_name', flat=True)
            statisctics = customer_info_panel.values_list('statisctic', flat=True)
            files_area_name = customer_info_panel.values_list('file_area_name', flat=True)
            
            if file_area:
                if file_area[0]:
                    files_infopanel = [n for n in file_area]
            
            if attribute_name:
                if attribute_name[0] and dirs_list:
                    dirs_infopanel = [n for n in attribute_name]
                    
            if statisctics:
                if statisctics[0]:
                    statisctics_infopanel = [n for n in statisctics]

        # print 'show_file ================================= ', show_file

        if show_file:
            if CustomerInfoPanel.objects.filter(
                    user=request.user, data_set=data_set, file_area_name=show_file).exists():
                try:
                    customer_info_panel_file = CustomerInfoPanel.objects.get(
                                                user=request.user,
                                                data_set=data_set,
                                                file_area_name=show_file)
                    file_tif = customer_info_panel_file.tif_path
                    file_png = customer_info_panel_file.png_path
                    url_png = customer_info_panel_file.url_png

                    # Convert tif to png

                    # Set file vars
                    # # output_file = "out.jpg"
                    # # output_file_root = os.path.splitext(output_file)[0]
                    # output_file_ext = 'png'
                    # output_file_tmp = customer_info_panel_file.file_area_name + ".tmp"
                    #
                    # # Create tmp gtif
                    # driver = gdal.GetDriverByName("GTiff")
                    # dst_ds = driver.Create(output_file_tmp, 512, 512, 1, gdal.GDT_Byte )
                    # raster = numpy.zeros( (512, 512) )
                    # dst_ds.GetRasterBand(1).WriteArray(raster)
                    #
                    # # Create jpeg or rename tmp file
                    # if (cmp(output_file_ext.lower(),"png" ) == 0):
                    #     jpg_driver = gdal.GetDriverByName("PNG")
                    #     jpg_driver.CreateCopy( file_png, dst_ds, 0 )
                    #     os.remove(output_file_tmp)
                    # else:
                    #     os.rename(output_file_tmp, file_png)

                    try:
                        check_date = check_date_files(file_tif, file_png)

                        if check_date:
                            if os.path.exists(file_tif):
                                # check_call(('cat {0} | convert - {1}').format(file_tif, file_png), shell=True)
                                ##
                                proc = Popen(['cat', file_tif], stdout=PIPE)
                                p2 = Popen(['convert', '-', file_png], stdin=proc.stdout)

                                while not os.path.exists(file_png):
                                    pass
                                    # print 'while os.path.exists(file_png) =============================================='

                                ## gdal_translate -of JPEG -scale -co worldfile=yes input.tiff output.jpg
                                # check_call(('gdal_translate -of JPEG -scale -co worldfile=yes {0} {1}').format(file_tif, file_png), shell=True)
                            else:
                                warning_message = u'The images "{0}" does not exist!'.\
                                                    format(customer_info_panel_file.file_area_name)
                    except Exception, e:
                        print 'Popen Exception =============================== ', e

                    # get the lat/lon values for a GeoTIFF files
                    try:
                        ds = gdal.Open(file_tif)
                        width = ds.RasterXSize
                        height = ds.RasterYSize
                        gt = ds.GetGeoTransform()
                        minx = gt[0]
                        miny = gt[3] + width*gt[4] + height*gt[5]
                        maxx = gt[0] + width*gt[1] + height*gt[2]
                        maxy = gt[3]
                        centery = (maxy + miny) / 2
                        centerx = (maxx + minx) / 2

                        cLng = centerx
                        cLat = centery
                        eLat_1 = miny
                        eLng_1 = minx
                        eLat_2 = maxy
                        eLng_2 = maxx
                        google_map_zoom = GOOGLE_MAP_ZOOM
                    except AttributeError, e:
                        print 'GDAL AttributeError =============================== ', e
                except CustomerInfoPanel.DoesNotExist, e:
                    print 'CustomerInfoPanel.DoesNotExist =============================== ', e
                    warning_message = u'The file "{0}" does not exist. Perhaps the data is outdated. Please refresh the page and try again.'.format(show_file)
                    # return HttpResponseRedirect(
                    #     u'%s?danger_message=%s' % (reverse('customer_section'),
                    #     (u'The file "{0}" does not exist. Perhaps the data is outdated. Please refresh the page and try again.'.format(show_file)))
                    # )

    if show_file:
        try:
            file_tif_path = CustomerInfoPanel.objects.get(
                                user=request.user,
                                data_set=data_set,
                                file_area_name=show_file).tif_path
            # file_tif_path = show_file + '.tif'
            
            attribute, units = getAttributeUnits(request.user, show_file)
        except Exception:
            pass
        
    # Get the polygons list from media folder
    try:
        root, dirs, files = os.walk(polygons_path).next()
        
        for pol in customer_polygons:
            if pol.kml_name in files:
                file_extension = os.path.splitext(pol.kml_name)
                polygons.append(pol)
            else:
                pol.delete()
    except Exception, e:
        print 'Exception 02 ========================= ', e
        warning_message = u'The polygon directory "{0}" does not exist!'.format(polygons_path)
    
    if show_file:
        try:
            #  data_set_id
            # ds = DataSet.objects.get(id=data_set_id)
            # cust_inf_panel = CustomerInfoPanel.objects.get(user=request.user, file_area_name=show_file)
            
            shelf_dt = ShelfData.objects.get(attribute_name=attribute, units=units)
            show_totals = shelf_dt.show_totals
            # print 'customer_info_panel.file_area_name =================== ', cust_inf_panel.file_area_name
            # print 'customer_info_panel.data_set =================== ', cust_inf_panel.data_set
            # print 'show_file =================== ', show_file
            # print 'show_file =================== ', show_file
            # print 'attribute =================== ', attribute
            # print 'show_totals =================== ', shelf_dt.show_totals
        except ShelfData.DoesNotExist:
            pass
    
    data = {
        'title': title,
        'customer': customer,
        'url_name': url_name,
        'warning_message': warning_message,
        'customer_info_panel': customer_info_panel,

        'info_panel': info_panel,

        'data_set_id': data_set_id,
        'data_sets': data_sets,
        'dirs_list': dirs_list,
        'files_infopanel': files_infopanel,
        'dirs_infopanel': dirs_infopanel,
        'statisctics_infopanel': statisctics_infopanel,
        'show_file': show_file,
        'file_tif_path': file_tif_path,
        'polygons': polygons,
        'absolute_kml_url': absolute_kml_url,
        'attribute': attribute,
        'units': units,
        'show_totals': show_totals,
        
        'php_query': php_query,

        'cLng': cLng,
        'cLat': cLat,
        'eLat_1': eLat_1,
        'eLng_1': eLng_1,
        'eLat_2': eLat_2,
        'eLng_2': eLng_2,
        'absolute_url_png_file': url_png,
        'GOOGLE_MAP_ZOOM': google_map_zoom,
    }

    return data
    

# PHP calculations
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/customer_section_php.html')
def customer_section_php(request):
    title = 'PHP page'
    file_tif_path = ''
    coord_list = []
    latlist = ''
    lonlist = ''
    customer = request.user
    customer_tmp_file = str(customer) + '_result.csv'
    php_file = '{0}_php_tmp.txt'.format(customer)
    file_path_php = os.path.join(KML_PATH, php_file)
    tmp_file_path = os.path.join(TMP_PATH, customer_tmp_file)
    result_f_name = 'src/media/temp_files/{0}_result.csv'.format(customer)
    
    ####################### write log file
    log_file = '/home/gsi/LOGS/delete_file.log'
    log_delete_file = open(log_file, 'w+')
    log_delete_file.write('FILE NAME: '+result_f_name+'\n')
    #######################
    
    # print 'tmp_file_path ============================== ', tmp_file_path
    
    # $latlist = '48.88672158743591,48.86956150482169,48.84019508397442';
    # $lonlist = '-89.83619749546051,-89.57595884799957,-89.75036680698395';
    
    # Handling GET request
    if request.method == "GET":
        data_get = request.GET
        
        # print 'data_get ============================= ', data_get
        
        if data_get.get('tif_path'):
            file_tif_path = data_get.get('tif_path')
            
            try:
                os.remove(tmp_file_path)
                
                ####################### write log file
                log_delete_file.write('remove FILE: "{0}"'.format(tmp_file_path))
                ####################### write log file
            except Exception, e:
                print 'except REMOVE FILE =========================== ', e
                ####################### write log file
                log_delete_file.write('ERROR remove FILE: "{0}"'.format(e))
                ####################### write log file
                pass
            
            
            f_php_coord = open(file_path_php)
            for line in f_php_coord.readlines():
                coord_list.append(line.replace('\n',''))
                
            # print 'coord_list ============================= ', coord_list
            
            latlist = coord_list[0]
            lonlist = coord_list[1]
            
            # print 'latlist =========================== ', latlist
            # print 'lonlist =========================== ', lonlist
    
    ####################### END write log file
    log_delete_file.close()
    #######################
    
            
    data = {
        'title': title,
        'file_tif_path': file_tif_path,
        'latlist': latlist,
        'lonlist': lonlist,
        'result_f_name': result_f_name,
    }

    return data
    
    
# Delete TMP file
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/customer_delete_file.html')
def customer_delete_file(request):
    title = ''
    customer = request.user
    result_f_name = str(customer) + '_result.csv'
    
    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get_ajax = request.GET
        
        # print 'data_get AJAX ============================= ', data_get_ajax
        
        ####################### write log file
        log_file = '/home/gsi/LOGS/create_file.log'
        log_create_file = open(log_file, 'w+')
        #######################
        
        if data_get_ajax.get('delete_file'):
            tmp_file_path = os.path.join(TMP_PATH, result_f_name)
            while not os.path.exists(tmp_file_path):
                print 'NO FILE ==================================='
                pass
                
            data = '/media/temp_files/' + result_f_name
            
            # print 'FILE exists ==================================='
        
            return HttpResponse(data)
        
    data = {
        'title': title,
    }

    return data
