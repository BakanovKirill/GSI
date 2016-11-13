# -*- coding: utf-8 -*-
""" urls.py """
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^$', 'wiki.views.wiki', name='wiki'),
]
