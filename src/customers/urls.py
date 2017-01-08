# -*- coding: utf-8 -*-
"""Customers app urls.py"""

from django.conf.urls import include, url
# from django.views.generic.base import RedirectView


urlpatterns = [
    # the url for the categorys list
	url(r'^category/show$', 'customers.views.categorys_list', name='categorys_list'),

	# the url for the category add
	url(r'^category/add$', 'customers.views.category_add', name='category_add'),

	# the url for the category edit
	url(r'^category/(?P<category_id>\d+)/edit$', 'customers.views.category_edit', name='category_edit'),

	# the url for the shelf_data list
	url(r'^shelf-data/show$', 'customers.views.shelf_data_list', name='shelf_data_list'),

	# the url for the shelf_data add
	url(r'^shelf-data/add$', 'customers.views.shelf_data_add', name='shelf_data_add'),

	# the url for the shelf_data edit
	url(r'^shelf-data/(?P<shelf_data_id>\d+)/edit$', 'customers.views.shelf_data_edit', name='shelf_data_edit'),
]
