# -*- coding: utf-8 -*-
"""Views for the customers app."""
from django.shortcuts import render
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from customers.models import Category, ShelfData
from core.paginations import paginations
from customers.customers_update_create import category_update_create, shelf_data_update_create
from core.get_post import get_post
from customers.customers_forms import CategoryForm, ShelfDataForm


# categorys list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/categorys_list.html')
def categorys_list(request):
    """**View all categories in Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The categorys for the Shelf Data'
    url_name = 'categorys'
    but_name = 'static_data'

    categorys = Category.objects.all()
    category_name = ''

    # Sorted by name
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
        # if request.POST.get('delete_button'):
        if request.POST.get('category_select'):
            for category_id in request.POST.getlist('category_select'):
                cur_category = get_object_or_404(Category, pk=category_id)
                category_name += '"' + cur_category.name + '", '
                cur_category.delete()

            category_ids = '_'.join(request.POST.getlist('env_select'))

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


# category_ add
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
        'save_button': 'categorys_list',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys_list'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'static_data'
    available_tiles = Category.objects.all()

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


# category_ edit
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
        'save_button': 'categorys_list',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys_list'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'static_data'

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


# categorys list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/shelf_data_list.html')
def shelf_data_list(request):
    """**View all Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The Shelf Data'
    url_name = 'shelf_data'
    but_name = 'static_data'

    shelf_data = ShelfData.objects.all()
    shelf_data_name = ''

    # Sorted by name
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
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(ShelfData, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        # if request.POST.get('delete_button'):
        if request.POST.get('shelf_data_select'):
            for shelf_data_id in request.POST.getlist('shelf_data_select'):
                cur_shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
                shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
                cur_shelf_data.delete()

            shelf_data_ids = '_'.join(request.POST.getlist('env_select'))

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


# category_ add
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
        'save_button': 'shelf_data_list',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data_list'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'static_data'
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


# category_ edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_edit(request, shelf_data_id):
    """**View for the "ShelfData "<attribute_name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *category_id:* The ShelfData object ID
    """

    shelf_data = get_object_or_404(ShelfData, pk=category_id)
    title = 'Category Edit "%s"' % (shelf_data.attribute_name)
    url_form = 'shelf_data_edit'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data_list',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data_list'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'static_data'

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
