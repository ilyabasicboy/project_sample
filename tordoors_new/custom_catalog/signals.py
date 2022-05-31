# -*- encoding: utf-8 -*-
from mptt.signals import node_moved
from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from catalog.models import TreeItem
from tordoors_new.custom_catalog.models import Product, Value, Section, Category, Parameter, Property


def catalog_changed_handler(sender, instance, **kwargs):

    """ Логика очистки кэша после изменения каталога """

    cache.clear()


post_save.connect(catalog_changed_handler, sender=Section)
post_save.connect(catalog_changed_handler, sender=Product)
pre_delete.connect(catalog_changed_handler, sender=Section)
pre_delete.connect(catalog_changed_handler, sender=Product)
node_moved.connect(catalog_changed_handler, sender=TreeItem)


def create_parameter(sender, instance, **kwargs):

    " Обновление параметров товаров/разделов/категорий при сохранении свойства "

    default_values = instance.values.filter(default=True)

    # Дефолтное значение свойства, если такое есть
    value = default_values[0] if default_values.exists() and not instance.optional else None

    """ Товары """
    items = Product.objects.exclude(product_parameters__property=instance)
    for item in items:
        item.product_parameters.create(
            property=instance,
            value=value,
        )
    # То же самое с доп. параметрами
    items = Product.objects.exclude(product_add_parameters__property=instance)
    for item in items:
        item.product_add_parameters.create(
            property=instance
        )

    """ Разделы """
    sections = Section.objects.exclude(section_parameters__property=instance)
    for section in sections:
        section.section_parameters.create(
            property=instance,
            value=value,
        )
    # То же самое с доп. параметрами
    sections = Section.objects.exclude(section_add_parameters__property=instance)
    for section in sections:
        section.section_add_parameters.create(
            property=instance,
        )

    """ Категории """
    categories = Category.objects.exclude(category_parameters__property=instance)
    for category in categories:
        category.category_parameters.create(
            property=instance,
            value=value,
        )

post_save.connect(create_parameter, sender=Property)


def create_product_parameters(sender, instance, **kwargs):
    " Создание параметров при сохранении товара "
    for property in Property.objects.all():
        value = property.values.filter(default=True)[0] \
            if property.values.filter(default=True).exists() and not property.optional else None
        if not instance.product_parameters.filter(property=property).exists():
            instance.product_parameters.create(
                property=property,
                value=value
            )
        if not instance.product_add_parameters.filter(property=property).exists():
            # Создать доп параметры товара
            instance.product_add_parameters.create(
                property=property
            )

post_save.connect(create_product_parameters, sender=Product)


def create_section_parameters(sender, instance, **kwargs):

    " Создание параметров при сохранении раздела "

    for property in Property.objects.all():
        value = property.values.filter(default=True)[0] \
            if property.values.filter(default=True) and not property.optional else None
        if not instance.section_parameters.filter(property=property).exists():
            instance.section_parameters.create(
                property=property,
                value=value
            )
        if not instance.section_add_parameters.filter(property=property).exists():
            #Создать доп параметры Раздела
            instance.section_add_parameters.create(
                property=property
            )

post_save.connect(create_section_parameters, sender=Section)


def create_category_parameters(sender, instance, **kwargs):

    " Создание параметров при сохранении категории "

    for property in Property.objects.all():
        if not instance.category_parameters.filter(property=property):
            value = property.values.filter(default=True)[0] \
                if property.values.filter(default=True) and not property.optional else None
            instance.category_parameters.create(
                property=property,
                value=value
            )

post_save.connect(create_category_parameters, sender=Category)


def set_default_value(sender, instance, **kwargs):
    """
    Заполнение пустых значений параметра
    при создании значения по умолчанию,
    если параметр обязательный
    """
    if instance.default and not instance.property.optional:
        parameters = Parameter.objects.filter(property=instance.property, value=None)
        for parameter in parameters:
            parameter.value = instance
            parameter.save()
        items = Product.objects.exclude(product_parameters__property=instance.property)
        for item in items:
            item.product_parameters.create(property=instance.property, value=instance)

post_save.connect(set_default_value, sender=Value)


def set_product_parameters(sender, instance, **kwargs):

    """
    Обновить суммарный список значений параметров у товаров
    (поле Product.parameters)
    """

    if instance.section:
        descendant_ids = instance.section.tree.get().get_descendants().filter(content_type__model='product').values_list('object_id')
        descendants = Product.objects.filter(id__in=descendant_ids)
        for product in descendants:
            values = Value.objects.filter(id__in=product.get_parameters().values_list('value', flat=True))
            product.parameters.set(values)
            product.save()

    elif instance.product:
        values = Value.objects.filter(id__in=instance.product.get_parameters().values_list('value', flat=True))
        instance.product.parameters.set(values)
        instance.product.save()

post_save.connect(set_product_parameters, sender=Parameter)