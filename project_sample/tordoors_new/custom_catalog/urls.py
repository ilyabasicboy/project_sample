# -*- coding: utf-8 -*-
from django.conf.urls import url

from tordoors_new.custom_catalog.views import FilterProductView

urlpatterns = [
    url(r'^filter_products/$', FilterProductView.as_view(), name='filter_products'),
]