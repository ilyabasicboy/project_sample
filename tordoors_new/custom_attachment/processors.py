# -*- coding: utf-8 -*-
from . import resizes
from attachment.processors import BottomRightWatermark, AroundWatermark, CenterWatermark, WatermarkBase
from imagekit.lib import Image
import math


class BottomLineWatermark(WatermarkBase):

    """ positioning watermark around the photo """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        mark = mark.resize(resize_watermark(img, mark))
        y = img.size[1] - mark.size[1]*2
        for x in range(0, img.size[0], mark.size[0]):
            layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)

def resize_watermark(im, mark):
    a = im.size[1]*0.1
    ratio = round(a/mark.size[1], 2)
    w = math.ceil(mark.size[0] * ratio)
    h = math.ceil(mark.size[1] * ratio)
    return (w, h)


class Watermark(BottomLineWatermark):
    image_path = None
    opacity = 1