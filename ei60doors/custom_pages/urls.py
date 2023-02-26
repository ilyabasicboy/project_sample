# -*- coding: utf-8 -*-
from django.conf.urls import url
from ei60doors.custom_pages.views import pages_list_pagination

urlpatterns = [
    url(r'^pages_list/(?P<obj_id>\d+)/$', pages_list_pagination, name='pages_list'),
]
