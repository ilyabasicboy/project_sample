
# -*- coding: utf-8 -*-
from . import resizes
from attachment.processors import AroundWatermark
from itertools import cycle
from imagekit.lib import Image
import math


def filebrowser_processor(img, verbose_name):

    """ Применение файлбраузером процессоров из attachments """

    ResizeClass = getattr(resizes, 'Resize' + verbose_name)
    img, fmt = ResizeClass.process(img, img.format, None)
    return img


class CustomWatermark(AroundWatermark):

    """ positioning watermark around the photo """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        mark = mark.resize(resize_watermark(img, mark))
        cycled_distance = cycle([img.size[0]/2-mark.size[0]/2, img.size[0]/2-mark.size[0]/2-mark.size[0]])
        for y in range(mark.size[1], img.size[1], mark.size[1]*2):
            for x in range(int(next(cycled_distance)), img.size[0], int(mark.size[0])*2):
                layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)


def resize_watermark(im, mark):
    a = im.size[1]*0.08
    ratio = round(a/mark.size[1], 2)
    w = math.ceil(mark.size[0] * ratio)
    if not w:
        w = 1
    h = math.ceil(mark.size[1] * ratio)
    if not h:
        h = 1
    return (w, h)
