"""GSI URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

# -*- coding: utf-8 -*-
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),

	# index
	url(r'^$', 'gsi.views.index', name='index'),

	# upload file
	url(r'^upload-file/$', 'gsi.views.upload_file', name='upload_file'),

	# run base
	url(r'^run/setup/$', 'gsi.views.run_setup', name='run_setup'),
	url(r'^run/new/$', 'gsi.views.new_run', name='new_run'),
	url(r'^run/(?P<run_id>\d+)/$', 'gsi.views.run_update', name='run_update'),

	# run base view results
	url(r'^run/(?P<run_id>\d+)/view-results/$', 'gsi.views.view_results', name='view_results'),

	# run base view folder results
	url(r'^run/(?P<run_id>\d+)/view-results/(?P<prev_dir>[%\w]+)/(?P<dir>\w+)/$',
		'gsi.views.view_results_folder', name='view_results_folder'),

	# submit a run
	url(r'^run/submit/$', 'gsi.views.submit_run', name='submit_run'),

	# run progress
	url(r'^run/progress/$', 'gsi.views.run_progress', name='run_progress'),

	# run details
	url(r'^run/details/(?P<run_id>\d+)/$', 'gsi.views.run_details', name='run_details'),

	# sub cards of card run details
	url(r'^run/(?P<run_id>\d+)/carditem/(?P<card_id>\d+)/details/$', 'gsi.views.sub_card_details', name='sub_card_details'),

	# log view cards
	url(r'^run/(?P<run_id>\d+)/card/(?P<card_id>\d+)/log/(?P<status>\w+)/$', 'gsi.views.view_log_file', name='view_log_file'),

	# log view sub cards
	url(r'^run/(?P<run_id>\d+)/card/(?P<card_id>\d+)/subcard/log/(?P<count>\d+)/(?P<status>\w+)/$',
		'gsi.views.view_log_file_sub_card', name='view_log_file_sub_card'),

	# setup home variable
	url(r'^run/home-variable/setup/$', 'gsi.views.home_variable_setup', name='home_variable_setup'),

	# audit history
	url(r'^run/(?P<run_id>\d+)/audit-history/$', 'gsi.views.audit_history', name='audit_history'),

	# environment groups
	url(r'^run/environment-groups/$', 'gsi.views.environment_groups', name='environment_groups'),

	# environment groups edit
	url(r'^run/environment-group/add/$', 'gsi.views.environment_group_add', name='environment_group_add'),
	url(r'^run/environment-group/(?P<env_id>\d+)/$', 'gsi.views.environment_group_edit', name='environment_group_edit'),

	# areas
	url(r'^areas/list/$', 'gsi.views.areas', name='areas'),

	# areas edit
	url(r'^area/add/$', 'gsi.views.area_add', name='area_add'),
	url(r'^area/(?P<area_id>\d+)/$', 'gsi.views.area_edit', name='area_edit'),

	# years group
	url(r'^years-group/list/$', 'gsi.views.years_group', name='years_group'),

	# years group edit
	url(r'^year-group/add/$', 'gsi.views.years_group_add', name='years_group_add'),
	url(r'^year-group/(?P<yg_id>\d+)/$', 'gsi.views.years_group_edit', name='years_group_edit'),

	# satellite
	url(r'^satellites/list/$', 'gsi.views.satellite', name='satellite'),

	# satellite edit
	url(r'^satellite/add/$', 'gsi.views.satellite_add', name='satellite_add'),
	url(r'^satellite/(?P<satellite_id>\d+)/$', 'gsi.views.satellite_edit', name='satellite_edit'),

	# resolution
	url(r'^resolution/list/$', 'gsi.views.resolution', name='resolution'),

	# resolution edit
	url(r'^resolution/add/$', 'gsi.views.resolution_add', name='resolution_add'),
	url(r'^resolution/(?P<resolution_id>\d+)/$', 'gsi.views.resolution_edit', name='resolution_edit'),

	# tiles
	url(r'^tiles/list/$', 'gsi.views.tiles', name='tiles'),

	# tiles edit
	url(r'^tile/add/$', 'gsi.views.tile_add', name='tile_add'),
	url(r'^tile/(?P<tile_id>\d+)/$', 'gsi.views.tile_edit', name='tile_edit'),

	# years
	url(r'^years/list/$', 'gsi.views.years', name='years'),

	# years edit
	url(r'^year/add/$', 'gsi.views.year_add', name='year_add'),
	url(r'^year/(?P<year_id>\d+)/$', 'gsi.views.year_edit', name='year_edit'),

	# input_data_dir_list
	url(r'^input-data-dirs/list/$', 'gsi.views.input_data_dir_list', name='input_data_dir_list'),

	# input_data_dir_list edit
	url(r'^input-data-dir/add/$', 'gsi.views.input_data_dir_add', name='input_data_dir_add'),
	url(r'^input-data-dir/(?P<dir_id>\d+)/$', 'gsi.views.input_data_dir_edit', name='input_data_dir_edit'),

	# cards list
	url(r'^cards/list/$', 'gsi.views.cards_list', name='cards_list'),

	# Customer section
	url(r'^customer/$', 'gsi.views.customer_section', name='customer_section'),

	# Card Sequence edit
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.card_sequence_update', name='card_sequence_update'),


	# CARDS edit in the Run -------------------------------------------------------------------------------------------
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/qrf/(?P<qrf_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_qrf_edit', name='cs_runid_csid_qrf_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/rfscore/(?P<rfscore_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_rfscore_edit', name='cs_runid_csid_rfscore_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/remap/(?P<remap_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_remap_edit', name='cs_runid_csid_remap_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/yearfilter/(?P<yf_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_year_filter_edit', name='cs_runid_csid_year_filter_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/collate/(?P<collate_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_collate_edit', name='cs_runid_csid_collate_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/preproc/(?P<preproc_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_preproc_edit', name='cs_runid_csid_preproc_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/mergecsv/(?P<mcsv_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_mergecsv_edit', name='cs_runid_csid_mergecsv_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/rftrain/(?P<rftrain_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_rftrain_edit', name='cs_runid_csid_rftrain_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/randomforest/(?P<rf_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_randomforest_edit', name='cs_runid_csid_randomforest_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/(?P<card_id>\d+)/calcstats/(?P<calcstats_id>\d+)/$',
		'gsi.views_card_runid_csid.cs_runid_csid_calcstats_edit', name='cs_runid_csid_calcstats_edit'),
	# -----------------------------------------------------------------------------------------------------------------


	# auth
	url(r'^logout/$', auth_views.logout, kwargs={'next_page': 'index'},
		name='auth_logout'),
	url(r'^register/complete/$', RedirectView.as_view(pattern_name='index'),
		name='registration_complete'),
	url(r'^', include('registration.backends.simple.urls', namespace='users')),

	# reset password option
	url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='reset_password_reset1'),
	url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),


	# api
	# url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
	# url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
	#	 name='update_run'),
	url(r'^run/(?P<run_id>\w+\.\w+\.\w+\.\w+\.\w+)/$', 'api.views.update_run',
		name='update_run'),

	# django-ckeditor
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
	url(r'^wiki/', include('articles.urls')),
	url(r'^cards/', include('cards.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
