# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *
from django.conf import settings
from tordoors_new.custom_attachment.processors import Watermark


class Watermark(Watermark):
    image_path = 'static/img/watermark.png'


class WatermarkPicture(ImageSpec):
    quality = 100
    processors = [Watermark,]


class Thumb(ImageSpec):
    processors = [ResizeThumb]


class Thumb300(ImageSpec):
    processors = [ResizeThumb300]


class Thumb500(ImageSpec):
    processors = [ResizeThumb500]


class Display(ImageSpec):
    processors = [ResizeDisplay]


class Img100x100(ImageSpec):
    # test spec
    quality = 50
    processors = [ResizeImg100x100]


class Img120x120(ImageSpec):
    processors = [ResizeImg120x120]


class ImgAutox200(ImageSpec):
    # test spec
    processors = [ResizeImgAutox200]


class Img300x300(ImageSpec):
    # test spec
    processors = [ResizeImg300x300]


class GallerySlider(ImageSpec):
    quality = 100
    processors = [ResizeGallerySlider]


class Gallery(ImageSpec):
    quality = 100
    processors = [ResizeGallery]


class ImgReview(ImageSpec):
    quality = 100
    processors = [ResizeImgReview]


class ImgListPages(ImageSpec):
    quality = 100
    processors = [ResizeImgListPages]


class ProductCard(ImageSpec):
    quality = 100
    processors = [ResizeProductCard]


class ProductView(ImageSpec):
    quality = 100
    processors = [ResizeProductView]


class ProductOption(ImageSpec):
    quality = 100
    processors = [ResizeProductOption]


class ProductInterior(ImageSpec):
    quality = 100
    processors = [ResizeProductInterior]


class Documents(ImageSpec):
    quality = 100
    processors = [ResizeDocuments]


class FlittingImg(ImageSpec):
    quality = 100
    processors = [ResizeFlittingImg]


class FlittingImgThumb(ImageSpec):
    quality = 100
    processors = [ResizeFlittingImgThumb]
