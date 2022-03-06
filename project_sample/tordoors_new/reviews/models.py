# -*- coding: utf-8 -*-
from django.db import models
import datetime
from attachment.settings import ATTACHMENT_UPLOAD_DIR
from os.path import join


REVIEW_IMG_UPLOAD = join(ATTACHMENT_UPLOAD_DIR, 'reviews')

# Create your models here.
class Review(models.Model):

    class IKOptions:
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        spec_module = 'tordoors_new.custom_attachment.ikspecs'
        cache_dir = join(ATTACHMENT_UPLOAD_DIR, 'cache')
        image_field = 'image'

    name = models.CharField(
        max_length=255,
        verbose_name=u'Имя',
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=255,
        verbose_name=u'Телефон',
        blank=True
    )
    email = models.CharField(
        max_length=255,
        verbose_name=u'E-mail',
        blank=True
    )
    image = models.FileField(
        verbose_name=u'Прикрепить Ваше фото',
        upload_to=REVIEW_IMG_UPLOAD,
        null=True, blank=True
    )
    date = models.DateField(
        verbose_name=u'Дата отправки отзыва',
        default=datetime.date.today()
    )
    content = models.TextField(
        max_length=2000,
        verbose_name=u'Текст отзыва'
    )
    show = models.BooleanField(
        verbose_name=u'Опубликовано',
        default=False
    )

    class Meta:
        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы'
        ordering = ('-date',)

    def __unicode__(self):
        return self.content[:50]