# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *
from pathlib import Path
from ei60doors.custom_attachment.processors import CustomWatermark
from django.conf import settings


class CustomImageSpec(ImageSpec):

    """ Added fix for png images """

    @classmethod
    def process(cls, image, obj):
        fmt = image.format
        img = image.copy()
        if img.mode != 'RGBA' and img.mode != 'RGB' and fmt != 'JPEG':
            img = img.convert('RGBA')
        for proc in cls.processors:
            img, fmt = proc.process(img, fmt, obj)
        img.format = fmt
        return img, fmt


class Watermark(CustomWatermark):
    STATIC_ROOT = Path(settings.STATIC_ROOT) if settings.STATIC_ROOT else Path('static')
    image_path = STATIC_ROOT / 'img/watermark.png'


class WatermarkPicture(CustomImageSpec):
    quality = 100
    processors = [Watermark]


class DivisionCard(CustomImageSpec):
    quality = 100
    processors = [ResizeDivisionCard]


class ProductCard(CustomImageSpec):
    quality = 100
    processors = [ResizeProductCard]


class ProductSlider(CustomImageSpec):
    quality = 100
    processors = [ResizeProductSlider]


class ProductThumb(CustomImageSpec):
    quality = 100
    processors = [ResizeProductThumb]


class GalleryDefault(CustomImageSpec):
    quality = 100
    processors = [ResizeGalleryDefault]


class GalleryGrid(CustomImageSpec):
    quality = 100
    processors = [ResizeGalleryGrid]


class Partners(CustomImageSpec):
    quality = 100
    processors = [ResizePartners]


class FacingMin(CustomImageSpec):
    quality = 100
    processors = [ResizeFacingMin]


class FacingBig(CustomImageSpec):
    quality = 100
    processors = [ResizeFacingBig]


class Thumb(CustomImageSpec):
    quality = 100
    processors = [ResizeThumb]


class PageCard(CustomImageSpec):
    quality = 100
    processors = [ResizePageCard]
