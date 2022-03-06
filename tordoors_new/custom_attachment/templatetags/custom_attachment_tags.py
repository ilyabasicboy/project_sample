# -*- coding: utf-8 -*-
from django import template


register = template.Library()

@register.filter
def role(images, role):
    """Get images with role"""
    try:
        return [image for image in images if image.role==role]
    except KeyError:
        return None
