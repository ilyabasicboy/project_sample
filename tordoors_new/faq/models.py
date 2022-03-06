# -*- coding: utf-8 -*-
from django.db import models
import datetime
from tinymce.models import HTMLField
from django.utils.timezone import now


class FaqTheme(models.Model):

    class Meta:
        verbose_name = u'тема вопроса'
        verbose_name_plural = u'темы вопросов'
        ordering = ('order_key',)

    order_key = models.PositiveIntegerField(verbose_name=u'', default=0, blank=False, null=False)
    name = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class FaqQuestion(models.Model):
    class Meta:
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'
        ordering = ('order_key',)

    order_key = models.PositiveIntegerField(verbose_name=u'', default=0, blank=True, null=True)
    name = models.CharField(verbose_name=u'Ваше имя', max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name=u'e-mail', max_length=50, blank=True)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)
    theme = models.ForeignKey(
        FaqTheme,
        verbose_name=u'Тема',
        on_delete=models.CASCADE,
    )
    question = models.CharField(verbose_name=u'Вопрос', max_length=2000)
    datetime = models.DateTimeField(verbose_name=u'Дата и время', default=now)
    answer = HTMLField(verbose_name=u'Ответ', max_length=4000, null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.name, self.question[:20])

    def __unicode__(self):
        return '%s : %s' % (self.name, self.question[:20])


