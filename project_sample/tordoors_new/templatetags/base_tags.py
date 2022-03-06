# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.html import strip_spaces_between_tags
from easy_news.models import News
from django.contrib.contenttypes.models import ContentType
from tordoors_new.custom_catalog.models import DocType

try:
    NEWS_CT = ContentType.objects.get_for_model(News)
except:
    pass

register = template.Library()


@register.inclusion_tag('parts/block_content.html')
def show_block_content(content):

    """ Отображение блока html-контента """

    return {'content': content}


def get_ranged_pagination_pages(current, pages, count):

    """ Возвращает список из count страниц пагинации вокруг текущего элемента
        count - четное кол-во элементов пагинации """

    result = pages
    if len(pages):
        first_page, last_page = pages[0], pages[-1]
        if count < last_page:
            step = count / 2
            left_page = current - step + 1
            right_page = current + step
            if left_page < first_page and right_page > last_page:
                pass
            elif left_page < first_page:
                right_page += (first_page - left_page)
                if right_page > last_page:
                    right_page = last_page
                left_page = first_page
            elif right_page > last_page:
                left_page -= right_page - last_page
                if left_page < first_page:
                    left_page = first_page
                right_page = last_page

            result = [i for i in range(left_page, right_page + 1)]
    return result


@register.simple_tag
def get_simple_custom_pagination(current, pages):

    """ Возвращает объект пагинации"""

    data = {}
    data['last'] = pages[-1]
    data['next'] = current + 1
    if data['next'] > data['last']:
       data['next'] = None
    return data


@register.simple_tag
def get_custom_pagination(current, pages):

    """ Возвращает объект пагинации"""

    data = {}
    data['pages'] = get_ranged_pagination_pages(current, pages, count=4)
    data['first'] = 1
    data['last'] = pages[-1]
    data['prev'] = current - 1
    if data['prev'] < data['first']:
        data['prev'] = None
    data['next'] = current + 1
    if data['next'] > data['last']:
       data['next'] = None
    return data


class SmartSpacelessNode(template.Node):

    """ Удалить пробелы из шаблона если отключен режим отладки """

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return content if settings.DEBUG else strip_spaces_between_tags(content.strip())


@register.tag
def smart_spaceless(parser, token):

    nodelist = parser.parse(('end_smart_spaceless',))
    parser.delete_first_token()
    return SmartSpacelessNode(nodelist)


@register.filter
def equal(val1, val2):

    """ Сравнение значений разных типов через приведение в юникод """

    return unicode(val1) == unicode(val2)


@register.simple_tag
def get_doc_types():
    """ Получить виды документов """
    return DocType.objects.exclude(image='')

@register.filter
def round_int(integer, number=None):
    print(round(integer, 3))
    return round(integer, number) if number else round(integer)


@register.filter
def price_format(val):

    """ Разделение разрядов числа пробелами """

    s = str(val)
    buf = ''
    result = ''
    for i in range(len(s)-1, -1, -1):
        buf = s[i] + buf
        if len(buf) == 3:
            result = buf + ' ' + result
            buf = ''
    if len(buf):
        result = buf + ' ' + result
    return result