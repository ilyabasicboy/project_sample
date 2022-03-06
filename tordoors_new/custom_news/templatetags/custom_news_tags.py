# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from attachment.models import AttachmentImage
from tordoors_new.custom_news.models import NewsRoot
from ..models import CustomNews


try:
    NEWS_CT = ContentType.objects.get_for_model(CustomNews)
except:
    pass

register = template.Library()


@register.inclusion_tag('custom_news/parts/block_cards.html', takes_context=True)
def show_block_news(context, ):

    """ Отображает блок новостей """

    news = CustomNews.objects.filter(show=True).order_by('-date')

    context['object_list'] = news

    return context


@register.simple_tag()
def get_news_root():

    """ Возвращает корневую новостей """

    return NewsRoot.objects.all().first()


@register.simple_tag
def get_news(num=None, current_new=None):
    news = CustomNews.objects.filter(show=True).order_by('-date', 'title')
    if current_new:
        news = news.exclude(id=current_new.id)
    if num:
        news = news[:num]
    return news