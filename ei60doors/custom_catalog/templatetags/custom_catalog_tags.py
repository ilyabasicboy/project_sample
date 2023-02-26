# -*- coding: utf-8 -*-
from django import template
from ei60doors.custom_catalog.utils import get_model_field
from ei60doors.custom_catalog.models import GROUP_CHOICES, Section, Category
from itertools import chain
from catalog.utils import get_sorted_content_objects
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_inherited_field(object, attr, display=False, many_to_many=False):
    """
    param object - ModelObject
    param attr - string field name

    Returns field value inherited by catalog tree
    """
    return get_model_field(object, attr, display, many_to_many)


@register.simple_tag()
def get_grouped_catalog_items():
    result = {}
    for group in GROUP_CHOICES:
        result[group[1]] = list(
            chain(
                Section.objects.filter(group=group[0], show=True),
                Category.objects.filter(group=group[0], show=True)
            )
        )
    return result


@register.simple_tag()
def get_sorted_categories_and_sections():
    categories = get_sorted_content_objects(
        Category.objects.filter(show=True)
    )
    sections = get_sorted_content_objects(
        Section.objects.filter(show=True)
    )
    return list(chain(categories, sections))


@register.simple_tag()
def get_add_images(object):

    # add. images for slider in product page
    result = AttachmentImage.objects.none()
    object_ct = ContentType.objects.get_for_model(object)
    add_images = AttachmentImage.objects.filter(
        object_id=object.id,
        content_type=object_ct,
        role=settings.ROLE_ADD_IMAGE
    )
    if add_images:
        result = add_images
    else:
        try:
            parent = object.tree.get().parent.content_object
            parent_ct = ContentType.objects.get_for_model(parent)
            result = AttachmentImage.objects.filter(
                object_id=parent.id,
                content_type=parent_ct,
                role=settings.ROLE_ADD_IMAGE
            )
        except:
            pass

    # add categories additional images
    categories_ids = object.category_set.all().values_list('id', flat=True)
    category_ct = ContentType.objects.get_for_model(Category)
    category__add_images = AttachmentImage.objects.filter(
        object_id__in=categories_ids,
        content_type=category_ct,
        role=settings.ROLE_ADD_IMAGE
    )
    if category__add_images:
        result = result | category__add_images
    return result
