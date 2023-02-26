# -*- coding: utf-8 -*-
from django.conf.urls import url
from ei60doors.custom_catalog.views import FilterProductView, popular_items_pagination

urlpatterns = [
    url(r'^filter_products/$', FilterProductView.as_view(), name='filter_products'),
    url(r'^novelties_list/$', popular_items_pagination, name='novelties_list'),
]
