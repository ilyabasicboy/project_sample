# -*- coding: utf-8 -*-
from . import resizes
from attachment.processors import BottomRightWatermark, AroundWatermark, CenterWatermark,WatermarkBase


def filebrowser_processor(img, verbose_name):

    """ Применение файлбраузером процессоров из attachments """

    ResizeClass = getattr(resizes, 'Resize' + verbose_name)
    img, fmt = ResizeClass.process(img, img.format, None)
    return img

class Watermark(AroundWatermark):
    image_path = None
    opacity = 1