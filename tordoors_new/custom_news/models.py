# -*- coding: utf-8 -*-
from django.db import models
from easy_news.models import News, MONTHS
from tinymce.models import HTMLField
from django.utils import timezone
from django.urls import reverse
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class CustomNews(News):

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    video = models.CharField(verbose_name=u'id после https://www.youtube.com/watch?v=', max_length=255, blank=True, null=True)

    def main_image(self):
        return AttachmentImage.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(CustomNews),
            role=settings.ROLE_COVER
        ).first()

    def add_images(self):
        return AttachmentImage.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(CustomNews),
            role=settings.ROLE_GALLERY
        )



class NewsRoot(models.Model):
    class Meta:
        verbose_name = u'Страница списка новостей'
        verbose_name_plural = verbose_name

    title = models.CharField(verbose_name=u'заголовок', max_length=300)
    last_modified = models.DateTimeField(auto_now=True)
    main_content = HTMLField(verbose_name=u'контент', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент внизу страницы', default='', blank=True)

    @property
    def news(self):

        """ Возвращает список новостей """

        return CustomNews.objects.filter(show=True, date__lte=timezone.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_root')



