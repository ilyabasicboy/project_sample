# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.shortcuts import render
from pages.models import Page
from .models import ErrorPage
from ei60doors.custom_catalog.models import Root, Section, Category, Product


def handler404(request, exception=None):
    obj, _ = ErrorPage.objects.get_or_create(type='404')
    obj.generate_static_page(request)
    return render(request, 'service/404.html', {'object': obj}, status=404)


def handler500(request):
    obj, _ = ErrorPage.objects.get_or_create(type='500')
    obj.generate_static_page(request)
    return render(request, 'service/500.html', {'object': obj}, status=500)


def sitemap(request):
    sitemaps = {
        'pages': GenericSitemap({
            'queryset': Page.objects.filter(status=Page.PUBLISHED),
            'date_field': 'last_modification_date',
        }),
        'root': GenericSitemap({
            'queryset': Root.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'section': GenericSitemap({
            'queryset': Section.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'category': GenericSitemap({
            'queryset': Category.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'product': GenericSitemap({
            'queryset': Product.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
    }
    return sitemap_view(request, sitemaps, template_name='service/sitemap.xml')
