# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Logo(models.Model):
    class Meta:
        verbose_name = u'Логотип'
        verbose_name_plural = u'Логотипы'
        ordering = ['order_key', ]

    title = models.CharField(verbose_name=u'Название', max_length=100, blank=True, null=True)
    image = models.FileField(verbose_name=u'Адрес ссылки', max_length=100)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    order_key = models.PositiveIntegerField(verbose_name=u'', default=0, blank=False, null=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.title


class Advantage(models.Model):
    class Meta:
        verbose_name = u'Преимущество'
        verbose_name_plural = u'Преимущества'
        ordering = ['order_key', ]


    image = models.FileField(verbose_name=u'иконка')
    text = models.CharField(verbose_name=u'текст', max_length=255)
    bold_text = models.CharField(verbose_name=u'жирный текст', max_length=255)
    order_key = models.PositiveIntegerField(verbose_name=u'', default=0, blank=False, null=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.text