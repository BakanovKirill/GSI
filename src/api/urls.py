# -*- coding: utf-8 -*-
"""API urls.py"""

from django.conf.urls import include, url
from rest_framework.authtoken import views
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (DataSetList, DataSetDetail,
                        ShapeFileDetail, TimeSeriesDetail, TimeSeriesList,
                        UploadFileAoiView, UploadFileFtpView)


urlpatterns = [
	# API
	# url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
	# url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
	#	 name='update_run'),

	# api for the execute runs
	url(r'^run/(?P<run_id>\w+\.\w+\.\w+\.\w+\.\w+)/$', 'api.views.update_run', name='update_run'),
	# api for the gsi
	
	url(r'^external/login/', 'api.views.external_auth_api', name='external_auth_api'),
	url(r'^terraserver', 'api.views.terraserver', name='terraserver'),
	# url(r'^datasets/', 'api.views.datasets_list', name='datasets_list'),
	# url(r'^polygons/', CustomerPolygonsList.as_view()),
    url(r'^datasets/$', DataSetList.as_view()),
	url(r'^datasets/(?P<ds_id>[0-9]+)/$', DataSetDetail.as_view()),
	# url(r'^dataset/', 'api.views.dataset', name='dataset'),
   
    url(r'^shapefile/(?P<sf_id>[0-9]+)/$', ShapeFileDetail.as_view()), 
    url(r'^timeseries/$', TimeSeriesList.as_view()),
    url(r'^timeseries/(?P<ts_id>[0-9]+)/$', TimeSeriesDetail.as_view()),
   
    # upload AOI file
    url(r'^upload/(?P<ds_id>[0-9]+)/$', UploadFileAoiView.as_view()),

    # upload file to FTP
    url(r'^upload/$', UploadFileFtpView.as_view()),
	
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
