from django.conf.urls.static import static
from django.conf import settings

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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # temporary blocking
    url(r'^$', 'gsi.views.blocking', name='block'),


    # index
    url(r'^index/$', 'gsi.views.index', name='index'),


    # run base
    url(r'^run/setup/$', 'gsi.views.run_setup', name='run_setup'),
    url(r'^run/new/$', 'gsi.views.new_run', name='new_run'),
    url(r'^run/(?P<run_id>\d+)/$', 'gsi.views.run_update',
        name='run_update'),

    # submit a run
    url(r'^run/submit/$', 'gsi.views.submit_run', name='submit_run'),

    # execute run
    url(r'^run/execute/(?P<runs_id>\w+)/$', 'gsi.views.execute_runs', name='execute_runs'),


    # card sequence for ne run base
    url(r'^run/card-sequence/add/$', 'gsi.views.run_new_card_sequence_add',
        name='run_new_card_sequence_add'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.run_new_card_sequence_update',
        name='run_new_card_sequence_update'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/add/$', 'gsi.views.add_card_sequence',
        name='add_card_sequence'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.card_sequence_update',
        name='card_sequence_update'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/setup/$', 'gsi.views.card_sequence',
        name='card_sequence'),

    # -------------------------------------------------------------------- ???

    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/card-item/(?P<card_item_id>\d+)/$',
        'gsi.views.card_item_update', name='card_item_update'),


    # ------------------------------------------------------------------- ???


    # processing card
    url(r'^run/card-sequence/processing-card/add$',
        'cards.views.proces_card_new_run', name='proces_card_new_run'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/add$',
        'cards.views.proces_card_runid', name='proces_card_runid'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
        'cards.views.proces_card_runid_csid', name='proces_card_runid_csid'),

    # --------------------------------------------------------------------

    # url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/add$',
    #     'cards.views.proces_card_new_run_new_sc', name='proces_card_new_run_new_sc'),

    # url(r'^run/new/processing-card/$', 'cards.views.proces_card_new_run', name='proces_card_new_run'),

    # url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
    #     'cards.views.proces_card_sequence_card_edit', name='proces_card_sequence_card_edit'),

    # url(r'^run/(?P<run_id>\d+)/card-sequence/add/processing-card/$',
    #     'cards.views.proces_card_sequence_card_new', name='proces_card_sequence_card_new'),


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


    # auth
    url(r'^logout/$', auth_views.logout, kwargs={'next_page': 'index'},
        name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='index'),
        name='registration_complete'),
    url(r'^', include('registration.backends.simple.urls', namespace='users')),


    # api
    url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
    url(r'^run/(?P<run_id>\d+)/$', 'api.views.update_run', name='update_run'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
