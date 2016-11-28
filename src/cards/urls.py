# -*- coding: utf-8 -*-
""" urls.py """
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    # the url for the new processing card
	url(r'^run/card-sequence/processing-card/add$',
		'cards.views.proces_card_new_run', name='proces_card_new_run'),

	# the urls for the processing cards (runID card-sequenceID cards add)
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/add/$',
		'cards.views_card_runid_csid.runid_csid_qrf_add', name='runid_csid_qrf_add'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/add/$',
		'cards.views_card_runid_csid.runid_csid_rfscore_add', name='new_runid_csid_rfscore'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/add/$',
		'cards.views_card_runid_csid.runid_csid_remap_add', name='new_runid_csid_remap'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/add/$',
		'cards.views_card_runid_csid.runid_csid_year_filter_add', name='new_runid_csid_year_filter'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/add/$',
		'cards.views_card_runid_csid.runid_csid_collate_add', name='new_runid_csid_collate'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/add/$',
		'cards.views_card_runid_csid.runid_csid_preproc_add', name='new_runid_csid_preproc'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/add/$',
		'cards.views_card_runid_csid.runid_csid_mergecsv_add', name='new_runid_csid_mergecsv'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/add/$',
		'cards.views_card_runid_csid.runid_csid_rftrain_add', name='new_runid_csid_rftrain'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/add/$',
		'cards.views_card_runid_csid.runid_csid_randomforest_add', name='new_runid_csid_randomforest'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/calcstats/add/$',
		'cards.views_card_runid_csid.runid_csid_calcstats_add', name='new_runid_csid_calcstats'),


	# the urls for the editing processing cards (runID card-sequenceID cards edit)
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/(?P<qrf_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_qrf_edit', name='runid_csid_qrf_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_rfscore_edit', name='runid_csid_rfscore_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/(?P<remap_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_remap_edit', name='runid_csid_remap_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/(?P<yf_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_year_filter_edit', name='runid_csid_year_filter_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/(?P<collate_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_collate_edit', name='runid_csid_collate_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/(?P<preproc_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_preproc_edit', name='runid_csid_preproc_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_mergecsv_edit', name='runid_csid_mergecsv_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_rftrain_edit', name='runid_csid_rftrain_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/(?P<rf_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_randomforest_edit', name='runid_csid_randomforest_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/calcstats/(?P<calcstats_id>\d+)/$',
		'cards.views_card_runid_csid.runid_csid_calcstats_edit', name='runid_csid_calcstats_edit'),
]
