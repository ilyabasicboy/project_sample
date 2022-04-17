# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import x_robots_tag
from django.shortcuts import render
from easy_news.models import News
from pages.models import Page
from tordoors_new.custom_news.models import NewsRoot
from .models import ErrorPage
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.utils.http import http_date
from calendar import timegm
import datetime
from tordoors_new.custom_catalog.models import Section, Category, Root, Product


def handler404(request, exception=None):
    obj, _ = ErrorPage.objects.get_or_create(type='404')
    obj.generate_static_page(request)
    return render(request, 'service/404.html', {'object': obj}, status=404)


def handler500(request):
    obj, _ = ErrorPage.objects.get_or_create(type='500')
    obj.generate_static_page(request)
    return render(request, 'service/500.html', {'object': obj}, status=500)


# Переопределение функции, чтобы поменять scheme на https
@x_robots_tag
def sitemap_view(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = 'https'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
            if all_sites_lastmod:
                site_lastmod = getattr(site, 'latest_lastmod', None)
                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple() if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if all_sites_lastmod and lastmod is not None:
        # if lastmod is defined for all sites, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(timegm(lastmod))
    return response


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
        'sections': GenericSitemap({
            'queryset': Section.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'categories': GenericSitemap({
            'queryset': Category.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'products': GenericSitemap({
            'queryset': Product.objects.filter(show=True),
            'date_field': 'last_modified',
        }),
        'news': GenericSitemap({
            'queryset': News.objects.filter(show=True),
            'date_field': 'date',
        }),
        'news_root': GenericSitemap({
            'queryset': NewsRoot.objects.all(),
            'date_field': 'last_modified',
        }),
    }
    return sitemap_view(request, sitemaps, template_name='service/sitemap.xml')
