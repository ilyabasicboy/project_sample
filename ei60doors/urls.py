# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, path
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from pages import views as pages_views
from filebrowser.sites import site
from ei60doors.custom_catalog.xml import yml_export, xml_export, yml_direct


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('attachment.urls')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^products.yml$', yml_export),
    url(r'^direct-products.yml$', yml_direct),
    url(r'^google-products.xml$', xml_export),
    url(r'^custom_feedback/', include('ei60doors.custom_feedback.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^custom_catalog/', include('ei60doors.custom_catalog.urls')),
    url(r'^custom_pages/', include('ei60doors.custom_pages.urls')),
    url(r'^', include('ei60doors.service.urls')),
    url(r'^(?P<path>.*)/$', pages_views.details, name='pages-details-by-path'),
    url(r'^$', pages_views.details, name='pages-root', kwargs={'path': u''})
]

if settings.DEBUG:
    urlpatterns = [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


handler404 = 'ei60doors.service.views.handler404'
handler500 = 'ei60doors.service.views.handler500'

try:
    from ei60doors.service.models import SiteSettings
    site_settings = SiteSettings.objects.all().first()
    if site_settings:
        admin.site.site_header = site_settings.name
except:
    pass
