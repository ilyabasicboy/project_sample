# -*- coding:utf-8 -*-
from django.conf.urls import *
from .models import Review
from .forms import ReviewForm
from .views import submit_review, reviews_list
from django.views.generic.list import ListView

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', reviews_list, name='reviews'),
    url(r'^ajax/$', submit_review, name='ajax_reviewsubmit'),
]