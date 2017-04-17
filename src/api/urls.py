# -*- coding: utf-8 -*-
"""API urls.py"""

from django.conf.urls import include, url


urlpatterns = [
	# API
	# url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
	# url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
	#	 name='update_run'),

	# api for the execute runs
	url(r'^run/(?P<run_id>\w+\.\w+\.\w+\.\w+\.\w+)/$', 'api.views.update_run', name='update_run'),
	# api for the gsi
	# url(r'^snippets/$', views.snippet_list),
	url(r'^', 'api.views.api_terraserver', name='api_terraserver'),
	url(r'^datasets', 'api.views.api_datasets', name='api_datasets'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
