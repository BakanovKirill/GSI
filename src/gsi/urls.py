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

    # card sequence
    url(r'^run/(?P<run_id>\d+)/card-sequence/setup/$', 'gsi.views.card_sequence',
        name='card_sequence'),
    # url(r'^card-sequence/new/$', 'gsi.views.new_card_sequence', name='new_card_sequence'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.card_sequence_update',
        name='card_sequence_update'),
    # url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.current_card_sequence',
    #     name='current_card_sequence'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/add/$', 'gsi.views.add_card_sequence',
        name='add_card_sequence'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/card-item/(?P<card_item_id>\d+)/$',
        'gsi.views.card_item_update', name='card_item_update'),

    # processing card
    url(r'^run/new/processing-card/$', 'cards.views.proces_card_new_run', name='proces_card_new_run'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
        'cards.views.proces_card_sequence_card_edit', name='proces_card_sequence_card_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/add/processing-card/$',
        'cards.views.proces_card_sequence_card_new', name='proces_card_sequence_card_new'),

    # new run cards add
    url(r'^run/new/processing-card/qrf/add/$', 'cards.views_card_run.new_run_qrf',
        name='new_run_qrf'),
    url(r'^run/new/processing-card/rfscore/add/$', 'cards.views_card_run.new_run_rfscore',
        name='new_run_rfscore'),
    url(r'^run/new/processing-card/remap/add/$', 'cards.views_card_run.new_run_remap',
        name='new_run_remap'),
    url(r'^run/new/processing-card/year-filter/add/$', 'cards.views_card_run.new_run_year_filter',
        name='new_run_year_filter'),
    url(r'^run/new/processing-card/collate/add/$', 'cards.views_card_run.new_run_collate',
        name='new_run_collate'),
    url(r'^run/new/processing-card/preproc/add/$', 'cards.views_card_run.new_run_preproc',
        name='new_run_preproc'),
    url(r'^run/new/processing-card/mergecsv/add/$', 'cards.views_card_run.new_run_mergecsv',
        name='new_run_mergecsv'),
    url(r'^run/new/processing-card/rftrain/add/$', 'cards.views_card_run.new_run_rftrain',
        name='new_run_rftrain'),

    # new run cards edit
    url(r'^run/new/processing-card/qrf/(?P<qrf_id>\d+)/$',
        'cards.views_card_run.new_run_qrf_edit', name='new_run_qrf_edit'),
    url(r'^run/new/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
        'cards.views_card_run.new_run_rfscore_edit', name='new_run_rfscore_edit'),
    url(r'^run/new/processing-card/remap/(?P<remap_id>\d+)/$',
        'cards.views_card_run.new_run_remap_edit', name='new_run_remap_edit'),
    url(r'^run/new/processing-card/year-filter/(?P<yf_id>\d+)/$',
        'cards.views_card_run.new_run_year_filter_edit', name='new_run_year_filter_edit'),
    url(r'^run/new/processing-card/collate/(?P<collate_id>\d+)/$',
        'cards.views_card_run.new_run_collate_edit', name='new_run_collate_edit'),
    url(r'^run/new/processing-card/preproc/(?P<preproc_id>\d+)/$',
        'cards.views_card_run.new_run_preproc_edit', name='new_run_preproc_edit'),
    url(r'^run/new/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
        'cards.views_card_run.new_run_mergecsv_edit', name='new_run_mergecsv_edit'),
    url(r'^run/new/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
        'cards.views_card_run.new_run_rftrain_edit', name='new_run_rftrain_edit'),

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
