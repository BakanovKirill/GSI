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
    url(r'^setup-run/$', 'gsi.views.run_setup', name='run_setup'),
    url(r'^new-run/$', 'gsi.views.new_run', name='new_run'),
    url(r'^setup-run/edit/(?P<run_id>\d+)/$', 'gsi.views.run_update',
        name='run_update'),

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
