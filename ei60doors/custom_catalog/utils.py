from ei60doors.custom_catalog.models import Product, Section
from seo.models import Seo
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from attachment.models import AttachmentImage
from django.utils.encoding import smart_str
from django.conf import settings
from django.template.loader import render_to_string
import os
import re
from itertools import chain
from django.utils import timezone


def get_model_field(object, attr, display=False, many_to_many=False):
    """ Поиск атрибута модели по дереву каталога """
    try:
        if display:
            self_attr = getattr(object, attr)()
        elif many_to_many:
            self_attr = getattr(object, attr).all()
        else:
            self_attr = getattr(object, attr)
    except:
        self_attr = ''
    if self_attr:
        return self_attr
    else:
        try:
            return get_model_field(object.tree.get().parent.content_object, attr, display, many_to_many)
        except:
            return ''
    return ''


#Upload export_yml file
def save_export_yml():
    template = 'catalog/export_yml.xml'
    ct = ContentType.objects.get_for_model(Product)

    categories = Section.objects.filter(show=True)
    queryset = Product.objects.filter(
        show=True,
        price__gt=0,
        tree__parent__object_id__in=categories
    )

    items = []
    scheme = 'https://'
    domain = Site.objects.first()

    for door in queryset:
        section = door.tree.get().parent.content_object

        if section:
            seo = Seo.objects.filter(object_id=door.id, content_type=ct).first()
            seo_description = seo.description if seo else ' '

            door_images = AttachmentImage.objects.filter(content_type=ct.id, object_id=door.id)

            item = {
                "id": door.id,
                "url": "%s%s%s" % (scheme, domain, door.get_absolute_url()),
                "name": door.long_title if door.long_title else door.title,
                "description": seo_description,
                "price": door.price,
                "old_price": door.old_price,
                "pictures": door_images,
                "categoryId": section.id,
                'construciton': get_model_field(door, 'get_construction_display', display=True),
                'fireproof': get_model_field(door, 'get_fireproof_display', display=True),
                'readiness': get_model_field(door, 'readiness'),
                'delivery': get_model_field(door, 'delivery'),
                'mounting': get_model_field(door, 'mounting'),
                'habarytes': get_model_field(door, 'habarytes'),
                'specs': get_model_field(door, 'specs'),
                'domain': '%s%s' % (scheme, domain),
            }

            items.append(item)

    result = smart_str(render_to_string(template, {"items": items, "categories": categories, 'time': timezone.now()}))
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'export_yml.xml')
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, 'w') as f:
        f.write(result)


#Upload direct_yml file
def save_direct_yml():
    template = 'catalog/export_yml.xml'
    ct = ContentType.objects.get_for_model(Product)

    categories = Section.objects.filter(show=True)
    queryset = Product.objects.filter(
        show=True,
        price__gt=0,
        tree__parent__object_id__in=categories
    ).exclude(exclude_direct_yml=True)

    items = []
    scheme = 'https://'
    domain = Site.objects.first()

    for door in queryset:
        section = door.tree.get().parent.content_object

        if section:
            seo = Seo.objects.filter(object_id=door.id, content_type=ct).first()
            seo_description = seo.description if seo else ' '

            door_images = AttachmentImage.objects.filter(content_type=ct.id, object_id=door.id)

            item = {
                "id": door.id,
                "url": "%s%s%s" % (scheme, domain, door.get_absolute_url()),
                "name": door.long_title if door.long_title else door.title,
                "description": seo_description,
                "price": door.price,
                "old_price": door.old_price,
                "pictures": door_images,
                "categoryId": section.id,
                'construciton': get_model_field(door, 'get_construction_display', display=True),
                'fireproof': get_model_field(door, 'get_fireproof_display', display=True),
                'readiness': get_model_field(door, 'readiness'),
                'delivery': get_model_field(door, 'delivery'),
                'mounting': get_model_field(door, 'mounting'),
                'habarytes': get_model_field(door, 'habarytes'),
                'domain': '%s%s' % (scheme, domain)
            }

            items.append(item)

    result = smart_str(render_to_string(template, {"items": items, "categories": categories, 'time': timezone.now()}))
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'direct_yml.xml')
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, 'w') as f:
        f.write(result)


def save_export_xml():
    template = 'catalog/export_xml.xml'
    ct = ContentType.objects.get_for_model(Product)
    categories = Section.objects.filter(google_merchant=True, show=True).order_by('id')
    queryset = Product.objects.filter(show=True, price__gt=0).exclude(
        exclude_google_merchant=True
    )

    items = []
    scheme = 'https://'
    domain = Site.objects.filter().first()

    for door in queryset:
        try:
            section = door.tree.get().parent.content_object
        except:
            section = None

        google_merchant = get_model_field(door, 'google_merchant')
        if section and google_merchant:

            seo = Seo.objects.filter(object_id=door.id, content_type=ct).first()
            seo_description = seo.description if seo else ' '

            google_images = AttachmentImage.objects.filter(content_type=ct.id, object_id=door.id,
                                                           group__in=['google', 'Google'])
            door_images = AttachmentImage.objects.filter(content_type=ct.id, object_id=door.id, )

            item = {
                "id": door.id,
                "google_prefix": get_model_field(door, 'google_prefix'),
                "url": "%s%s%s" % (scheme, domain, door.get_absolute_url()),
                "name": door.long_title if door.long_title else door.title,
                "description": seo_description,
                "price": door.price,
                "old_price": door.old_price,
                'google_images': google_images,
                "images": door_images,
                'section': section,
                'domain': '%s%s' % (scheme, domain),
            }

            items.append(item)

    result = smart_str(render_to_string(template, {"items": items, "categories": categories, 'time': timezone.now()}))
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'export_xml.xml')
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, 'w') as f:
        f.write(result)
