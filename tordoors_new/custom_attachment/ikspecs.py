# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *
from django.conf import settings
from tordoors_new.custom_attachment.processors import Watermark


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


class Watermark(Watermark):
    image_path = 'static/img/watermark.png'


class WatermarkPicture(CustomImageSpec):
    quality = 100
    processors = [Watermark]


class Thumb(CustomImageSpec):
    quality = 100
    processors = [ResizeThumb]


class Thumb300(CustomImageSpec):
    quality = 100
    processors = [ResizeThumb300]


class Thumb500(CustomImageSpec):
    quality = 100
    processors = [ResizeThumb500]


class Display(CustomImageSpec):
    quality = 100
    processors = [ResizeDisplay]


class Img100x100(CustomImageSpec):
    quality = 100
    processors = [ResizeImg100x100]


class Img120x120(CustomImageSpec):
    processors = [ResizeImg120x120]


class ImgAutox200(CustomImageSpec):
    processors = [ResizeImgAutox200]


class Img300x300(CustomImageSpec):
    processors = [ResizeImg300x300]


class Produce(CustomImageSpec):
    quality = 100
    processors = [ResizeProduce]


class GallerySlider(CustomImageSpec):
    quality = 100
    processors = [ResizeGallerySlider]


class Gallery(CustomImageSpec):
    quality = 100
    processors = [ResizeGallery]


class ImgReview(CustomImageSpec):
    quality = 100
    processors = [ResizeImgReview]


class ImgListPages(CustomImageSpec):
    quality = 100
    processors = [ResizeImgListPages]


class ProductCard(CustomImageSpec):
    quality = 100
    processors = [ResizeProductCard]


class ProductView(CustomImageSpec):
    quality = 100
    processors = [ResizeProductView]


class ProductOption(CustomImageSpec):
    quality = 100
    processors = [ResizeProductOption]


class ProductInterior(CustomImageSpec):
    quality = 100
    processors = [ResizeProductInterior]


class Documents(CustomImageSpec):
    quality = 100
    processors = [ResizeDocuments]


class FlittingImg(CustomImageSpec):
    quality = 100
    processors = [ResizeFlittingImg]


class FlittingImgBig(CustomImageSpec):
    quality = 100
    processors = [ResizeFlittingImgBig]


class FlittingImgThumb(CustomImageSpec):
    quality = 100
    processors = [ResizeFlittingImgThumb]