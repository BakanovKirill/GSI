# -*- coding: utf-8 -*-
""" urls.py """
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from wiki.views import WikiUpdateView


urlpatterns = [
	url(r'^$', 'wiki.views.wiki_show', name='wiki_show'),
	# url(r'/(?P<wiki_id>\w+)/edit/^$', 'wiki.views.wiki_edit', name='wiki_edit'),
	url(r'^(?P<pk>\d+)/edit/$', WikiUpdateView.as_view(), name='wiki_edit'),
]
