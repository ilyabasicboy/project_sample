# -*- coding:utf-8 -*-
from imagekit.processors import Resize


class ResizeWatermarkPicture(Resize):
    height = 1200


class Resize80x56(Resize):
    width = 80
    height = 56
    crop = True


class ResizeThumb(Resize):
    width = 172
    height = 172


class ResizeThumb300(Resize):
    height = 300


class ResizeThumb500(Resize):
    height = 500


class ResizeDisplay(Resize):
    width = 1200
    height = 900


class ResizeImg300x300(Resize):
    width = 300
    height = 300
    crop = True


class ResizeImgAutox200(Resize):
    height = 200


class ResizeImg120x120(Resize):
    width = 120
    height = 120
    crop = True


class ResizeImg100x100(Resize):
    width = 100
    height = 100


class ResizeProduce(Resize):
    height = 500


class ResizeGallerySlider(Resize):
    height = 514


class ResizeGallery(Resize):
    height = 380


class ResizeImgReview(Resize):
    width = 280


class ResizeImgListPages(Resize):
    height = 200


class ResizeProductCard(Resize):
    height = 300


class ResizeProductView(Resize):
    height = 500


class ResizeProductOption(Resize):
    width = 280


class ResizeProductInterior(Resize):
    height = 700


class ResizeDocuments(Resize):
    height = 286


class ResizeFlittingImg(Resize):
    height = 280


class ResizeFlittingImgBig(Resize):
    height = 1000


class ResizeFlittingImgThumb(Resize):
    height = 80
