# -*- coding:utf-8 -*-
from imagekit.processors import Resize


class ResizeDivisionCard(Resize):
    height = 400


class ResizeProductSlider(Resize):
    height = 600


class ResizeProductThumb(Resize):
    height = 120


class ResizeProductCard(Resize):
    height = 360


class ResizeGalleryDefault(Resize):
    height = 400


class ResizeGalleryGrid(Resize):
    height = 600


class ResizePartners(Resize):
    height = 80


class ResizeFacingMin(Resize):
    height = 120


class ResizeFacingBig(Resize):
    height = 200


class ResizeThumb(Resize):
    width = 172
    height = 172


class ResizePageCard(Resize):
    width = 500
