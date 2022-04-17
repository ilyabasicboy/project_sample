# -*- coding: utf-8 -*-
from django import template
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects
from tordoors_new.custom_catalog.models import Product, Section, Category, Root, TYPE_CHOICES, Facing
from tordoors_new.custom_catalog.forms import FilterForm
from classytags.helpers import AsTag
from classytags.core import Options
from classytags.arguments import Argument
from itertools import chain
from pages.models import Page


register = template.Library()


@register.inclusion_tag('catalog/parts/block_cards.html', takes_context=True)
def show_block_cards(context):

    """ Возвращает список товаров """

    obj = context.get('object')
    products = obj.get_products()

    products_count = products.count()

    """ Добавление статей каждые 9 товаров """
    try:
        articles = obj.articles.all()
        if articles and len(products) >= 8:
            products = list(products)
            for i in range(int(len(products)/8)):
                products.insert(9*(i+1)-1, articles[i])
    except:
        pass

    context['object_list'] = products
    context['products_count'] = products_count
    return context


@register.inclusion_tag('catalog/parts/fast_filter_form.html', takes_context=True)
def show_filter_form(context, ajax=False):

    """ Форма для подбора по параметрам """

    form = FilterForm(initial=context.request.GET)
    object = context.get('object')
    c_type = ContentType.objects.get_for_model(object).model

    context['form'] = form
    context['object'] = object
    context['c_type'] = c_type
    context['ajax'] = ajax
    return context


@register.inclusion_tag('catalog/parts/short_filter_form.html', takes_context=True)
def show_short_filter_form(context, fast_filter=False):

    """ Форма для подбора по цене и сортировки """

    form = FilterForm(initial=context.request.GET)
    object = context.get('object')
    c_type = ContentType.objects.get_for_model(object).model

    context['object'] = object
    context['c_type'] = c_type
    context['form'] = form
    context['fast_filter'] = fast_filter
    return context


@register.simple_tag
def get_root():
    return Root.objects.first()


class GetCatalogMenuItems(AsTag):
    """ Возвращает список дочерних разделов и категорий """
    name = 'get_catalog_menu_items'
    options = Options(
        'for',
        Argument('parent', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context, parent):
        result = get_sorted_content_objects(
            get_content_objects(
                parent.tree.get().get_children().filter(
                    content_type__model__in=['section', 'category']
                )
            )
        )
        return result

register.tag(GetCatalogMenuItems)


@register.simple_tag
def get_fast_filter_page():
    return Page.objects.filter(template='pages/fast_filter.html').first()


@register.simple_tag
def get_similar_products(object):
    """ Возвращает товары из родительского раздела, исключая себя """
    if object.tree.get().parent:
        parent = object.tree.get().parent.content_object
        products = get_content_objects(
            parent.tree.get().get_descendants()\
                .filter(content_type__model='product')\
                .exclude(id=object.tree.get().id)[:10]
        )
        return products
    else:
        return []


@register.inclusion_tag('catalog/parts/catalog_main_menu.html', takes_context=True)
def catalog_main_menu(context):
    """ Меню в шапке сайта с разделами и категориями по типу изделия """
    section_list = {}
    root = Root.objects.all().first()
    if root:
        for type in TYPE_CHOICES:
            sections = Section.objects.filter(product_type=type[0], tree__parent=root.tree.get().id)
            categories = Category.objects.filter(product_type=type[0], tree__parent=root.tree.get().id)
            objects = get_sorted_content_objects(list(chain(sections, categories)))
            if objects:
                section_list[type[1]] = objects
        context['section_list'] = section_list
    return context


@register.simple_tag
def get_we_produce_sections():
    """ Товары для блока "Мы производим" """
    return Section.objects.filter(show_in_we_produce=True, show=True)


@register.simple_tag
def get_our_technologies():
    """ Товары для блока "Наши технологии" """
    sections = Section.objects.filter(show_in_our_technologies=True, show=True)
    categories = Category.objects.filter(show_in_our_technologies=True, show=True)
    return list(chain(sections, categories))


@register.simple_tag
def get_popular_products():
    """ Товары для блока "Популярные продукты" """
    return Product.objects.filter(popular=True, show=True)


def get_list(values):

    values = values[1:-1]
    values = [s for s in values.split(', ')]
    return values


@register.simple_tag
def get_products_by_id(product_ids):
    """ Возвращает товары по списку id """

    product_ids = get_list(product_ids)
    products = Product.objects.filter(id__in=product_ids, show=True)
    return products


@register.simple_tag
def get_facing_by_id(id):
    return Facing.objects.filter(id__in=id).first()


@register.simple_tag
def get_basic_parameters(object):
    return object.get_parameters().filter(property__show_on_item_desc=False)


@register.simple_tag
def get_last_products(num=20):
    return Product.objects.filter(show=True).order_by('-id')[:num]