# -*- coding: utf-8 -*-
""" urls.py """
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
	# url(r'^$', 'wiki.views.wiki', name='wiki'),
    # processing card
	url(r'^run/card-sequence/processing-card/add$',
		'cards.views.proces_card_new_run', name='proces_card_new_run'),

	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/add$',
		'cards.views.proces_card_runid', name='proces_card_runid'),

	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
		'cards.views.proces_card_runid_csid', name='proces_card_runid_csid'),


	# new runID card-sequenceID cards add
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/add/$',
		'cards.views_card_runid_csid.new_runid_csid_qrf', name='new_runid_csid_qrf'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/add/$',
		'cards.views_card_runid_csid.new_runid_csid_rfscore', name='new_runid_csid_rfscore'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/add/$',
		'cards.views_card_runid_csid.new_runid_csid_remap', name='new_runid_csid_remap'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/add/$',
		'cards.views_card_runid_csid.new_runid_csid_year_filter', name='new_runid_csid_year_filter'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/add/$',
		'cards.views_card_runid_csid.new_runid_csid_collate', name='new_runid_csid_collate'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/add/$',
		'cards.views_card_runid_csid.new_runid_csid_preproc', name='new_runid_csid_preproc'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/add/$',
		'cards.views_card_runid_csid.new_runid_csid_mergecsv', name='new_runid_csid_mergecsv'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/add/$',
		'cards.views_card_runid_csid.new_runid_csid_rftrain', name='new_runid_csid_rftrain'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/add/$',
		'cards.views_card_runid_csid.new_runid_csid_randomforest', name='new_runid_csid_randomforest'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/calcstats/add/$',
		'cards.views_card_runid_csid.new_runid_csid_calcstats', name='new_runid_csid_calcstats'),

	# new runID card-sequenceID cards edit
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/(?P<qrf_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_qrf_edit', name='new_runid_csid_qrf_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_rfscore_edit', name='new_runid_csid_rfscore_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/(?P<remap_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_remap_edit', name='new_runid_csid_remap_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/(?P<yf_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_year_filter_edit', name='new_runid_csid_year_filter_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/(?P<collate_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_collate_edit', name='new_runid_csid_collate_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/(?P<preproc_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_preproc_edit', name='new_runid_csid_preproc_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_mergecsv_edit', name='new_runid_csid_mergecsv_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_rftrain_edit', name='new_runid_csid_rftrain_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/(?P<rf_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_randomforest_edit', name='new_runid_csid_randomforest_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/calcstats/(?P<calcstats_id>\d+)/$',
		'cards.views_card_runid_csid.new_runid_csid_calcstats_edit', name='new_runid_csid_calcstats_edit'),

	# *****************************************************************************************************


	# new runID cards edit
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/qrf/(?P<qrf_id>\d+)/$',
		'cards.views_card_runid.new_runid_qrf_edit', name='new_runid_qrf_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
		'cards.views_card_runid.new_runid_rfscore_edit', name='new_runid_rfscore_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/remap/(?P<remap_id>\d+)/$',
		'cards.views_card_runid.new_runid_remap_edit', name='new_runid_remap_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/year-filter/(?P<yf_id>\d+)/$',
		'cards.views_card_runid.new_runid_year_filter_edit', name='new_runid_year_filter_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/collate/(?P<collate_id>\d+)/$',
		'cards.views_card_runid.new_runid_collate_edit', name='new_runid_collate_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/preproc/(?P<preproc_id>\d+)/$',
		'cards.views_card_runid.new_runid_preproc_edit', name='new_runid_preproc_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
		'cards.views_card_runid.new_runid_mergecsv_edit', name='new_runid_mergecsv_edit'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
		'cards.views_card_runid.new_runid_rftrain_edit', name='new_runid_rftrain_edit'),
	# url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/calcstats/(?P<calcstats_id>\d+)/$',
	#	 'cards.views_card_runid.new_runid_calcstats_edit', name='new_runid_calcstats_edit'),

	# --------------------------------------------------------------------

	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/add$',
		'cards.views.proces_card_run_new_csid', name='proces_card_run_new_csid'),

	# url(r'^run/new/processing-card/$', 'cards.views.proces_card_new_run', name='proces_card_new_run'),

	# url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
	#	 'cards.views.proces_card_sequence_card_edit', name='proces_card_sequence_card_edit'),

	# url(r'^run/(?P<run_id>\d+)/card-sequence/add/processing-card/$',
	#	 'cards.views.proces_card_sequence_card_new', name='proces_card_sequence_card_new'),


	# new run cards add
	url(r'^run/card-sequence/processing-card/qrf/add/$', 'cards.views_card_run.new_run_qrf',
		name='new_run_qrf'),
	url(r'^run/card-sequence/processing-card/rfscore/add/$', 'cards.views_card_run.new_run_rfscore',
		name='new_run_rfscore'),
	url(r'^run/card-sequence/processing-card/remap/add/$', 'cards.views_card_run.new_run_remap',
		name='new_run_remap'),
	url(r'^run/card-sequence/processing-card/year-filter/add/$', 'cards.views_card_run.new_run_year_filter',
		name='new_run_year_filter'),
	url(r'^run/card-sequence/processing-card/collate/add/$', 'cards.views_card_run.new_run_collate',
		name='new_run_collate'),
	url(r'^run/card-sequence/processing-card/preproc/add/$', 'cards.views_card_run.new_run_preproc',
		name='new_run_preproc'),
	url(r'^run/card-sequence/processing-card/mergecsv/add/$', 'cards.views_card_run.new_run_mergecsv',
		name='new_run_mergecsv'),
	url(r'^run/card-sequence/processing-card/rftrain/add/$', 'cards.views_card_run.new_run_rftrain',
		name='new_run_rftrain'),

	# new run cards edit
	url(r'^run/card-sequence/processing-card/qrf/(?P<qrf_id>\d+)/$',
		'cards.views_card_run.new_run_qrf_edit', name='new_run_qrf_edit'),
	url(r'^run/card-sequence/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
		'cards.views_card_run.new_run_rfscore_edit', name='new_run_rfscore_edit'),
	url(r'^run/card-sequence/processing-card/remap/(?P<remap_id>\d+)/$',
		'cards.views_card_run.new_run_remap_edit', name='new_run_remap_edit'),
	url(r'^run/card-sequence/processing-card/year-filter/(?P<yf_id>\d+)/$',
		'cards.views_card_run.new_run_year_filter_edit', name='new_run_year_filter_edit'),
	url(r'^run/card-sequence/processing-card/collate/(?P<collate_id>\d+)/$',
		'cards.views_card_run.new_run_collate_edit', name='new_run_collate_edit'),
	url(r'^run/card-sequence/processing-card/preproc/(?P<preproc_id>\d+)/$',
		'cards.views_card_run.new_run_preproc_edit', name='new_run_preproc_edit'),
	url(r'^run/card-sequence/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
		'cards.views_card_run.new_run_mergecsv_edit', name='new_run_mergecsv_edit'),
	url(r'^run/card-sequence/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
		'cards.views_card_run.new_run_rftrain_edit', name='new_run_rftrain_edit'),


	# new run card-sequenceID cards add
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/add/$',
		'cards.views_card_run_csid.new_run_csid_qrf', name='new_run_csid_qrf'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/add/$',
		'cards.views_card_run_csid.new_run_csid_rfscore', name='new_run_csid_rfscore'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/remap/add/$',
		'cards.views_card_run_csid.new_run_csid_remap', name='new_run_csid_remap'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/add/$',
		'cards.views_card_run_csid.new_run_csid_year_filter', name='new_run_csid_year_filter'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/collate/add/$',
		'cards.views_card_run_csid.new_run_csid_collate', name='new_run_csid_collate'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/add/$',
		'cards.views_card_run_csid.new_run_csid_preproc', name='new_run_csid_preproc'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/add/$',
		'cards.views_card_run_csid.new_run_csid_mergecsv', name='new_run_csid_mergecsv'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/add/$',
		'cards.views_card_run_csid.new_run_csid_rftrain', name='new_run_csid_rftrain'),

	# new run card-sequenceID cards edit
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/(?P<qrf_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_qrf_edit', name='new_run_csid_qrf_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_rfscore_edit', name='new_run_csid_rfscore_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/remap/(?P<remap_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_remap_edit', name='new_run_csid_remap_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/(?P<yf_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_year_filter_edit', name='new_run_csid_year_filter_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/collate/(?P<collate_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_collate_edit', name='new_run_csid_collate_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/(?P<preproc_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_preproc_edit', name='new_run_csid_preproc_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_mergecsv_edit', name='new_run_csid_mergecsv_edit'),
	url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
		'cards.views_card_run_csid.new_run_csid_rftrain_edit', name='new_run_csid_rftrain_edit'),


	# new runID cards add
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/qrf/add/$',
		'cards.views_card_runid.new_runid_qrf', name='new_runid_qrf'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rfscore/add/$',
		'cards.views_card_runid.new_runid_rfscore', name='new_runid_rfscore'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/remap/add/$',
		'cards.views_card_runid.new_runid_remap', name='new_runid_remap'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/year-filter/add/$',
		'cards.views_card_runid.new_runid_year_filter', name='new_runid_year_filter'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/collate/add/$',
		'cards.views_card_runid.new_runid_collate', name='new_runid_collate'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/preproc/add/$',
		'cards.views_card_runid.new_runid_preproc', name='new_runid_preproc'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/mergecsv/add/$',
		'cards.views_card_runid.new_runid_mergecsv', name='new_runid_mergecsv'),
	url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rftrain/add/$',
		'cards.views_card_runid.new_runid_rftrain', name='new_runid_rftrain'),
]
