# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from tordoors_new.custom_catalog.models import Product, Section, ProductImage
from django.shortcuts import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from seo.models import Seo
from tordoors_new.custom_catalog.utils import get_model_field


def yml_export(request):
    template = 'catalog/export_yml.yml'
    ct = ContentType.objects.get_for_model(Product)
    queryset = Product.objects.filter(show=True, price__gt=0)
    categories = Section.objects.filter(show=True).order_by('id')

    items = []
    if len(queryset):
        scheme = 'https://'
        domain = Site.objects.get_current()

        for door in queryset:

            if door.tree.get().parent:
                section = door.tree.get().parent.content_object

                seo = Seo.objects.filter(object_id=door.id, content_type=ct).first()
                if seo:
                    seo_description = seo.description if seo.description else ''

                item = {
                    "id": door.id,
                    "url": "%s%s%s" % (scheme, domain, door.get_absolute_url()),
                    "domain": domain,
                    "name": door.long_title if door.long_title else door.title,
                    "description": seo_description,
                    "price": door.price,
                    "square_price": door.price_per_square,
                    "pictures": ProductImage.objects.filter(product=door, side='outside'),
                    "categoryId": section.id,
                    'box_size': get_model_field(door, 'box_size'),
                    'production_time': door.production_time,
                    'guarantee': door.guarantee,
                    'facing': door.facing,
                    'parameters': door.get_parameters().filter(property__show_on_yml=True)
                }

                items.append(item)

    result = render_to_string(template, {"items": items, "categories": categories,}, request)
    return HttpResponse(result, content_type='text/xml')