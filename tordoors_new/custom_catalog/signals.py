# -*- encoding: utf-8 -*-
from mptt.signals import node_moved
from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from catalog.models import TreeItem
from tordoors_new.custom_catalog.models import Product, Value, Section, Category, Parameter,\
    AddParameter, Property, value_saved, object_saved, parameter_saved


def catalog_changed_handler(sender, instance, **kwargs):

    """ Логика очистки кэша после изменения каталога """

    cache.clear()


post_save.connect(catalog_changed_handler, sender=Section)
post_save.connect(catalog_changed_handler, sender=Product)
pre_delete.connect(catalog_changed_handler, sender=Section)
pre_delete.connect(catalog_changed_handler, sender=Product)
node_moved.connect(catalog_changed_handler, sender=TreeItem)


def create_parameter(sender, **kwargs):
    if isinstance(kwargs['object'], Property):
        """
        Добавление параметра при его сохранении
        если у товара/раздела/категории еще нет такого параметра.
        """

        default_values = kwargs['object'].values.filter(default=True)
        value = default_values[0] if default_values and not kwargs['object'].optional else None

        items = Product.objects.exclude(product_parameters__property=kwargs['object'])
        for item in items:
            item.product_parameters.create(
                property=kwargs['object'],
                value=value,
            )
        " Создать доп. параметры для товара "
        items = Product.objects.exclude(product_add_parameters__property=kwargs['object'])
        for item in items:
            item.product_add_parameters.create(
                property=kwargs['object']
            )

        sections = Section.objects.exclude(section_parameters__property=kwargs['object'])
        for section in sections:
            section.section_parameters.create(
                property=kwargs['object'],
                value=value,
            )
        " Создать доп. параметры для разделов "
        sections = Section.objects.exclude(section_add_parameters__property=kwargs['object'])
        for section in sections:
            section.section_add_parameters.create(
                property=kwargs['object'],
            )

        categories = Category.objects.exclude(category_parameters__property=kwargs['object'])
        for category in categories:
            category.category_parameters.create(
                property=kwargs['object'],
                value=value,
            )

    if isinstance(kwargs['object'], Value):
        """
        Заполнение пустых значений параметра 
        при создании значения по умолчанию,
        если параметр обязательный 
        """
        if kwargs['default'] and not kwargs['property'].optional:
            parameters = Parameter.objects.filter(property=kwargs['property'], value=None)
            for parameter in parameters:
                parameter.value = kwargs['object']
                parameter.save()
            items = Product.objects.exclude(product_parameters__property=kwargs['property'])
            for item in items:
                item.product_parameters.create(property=kwargs['property'], value=kwargs['object'])
    elif isinstance(kwargs['object'], Product):
        " Создание существующих параметров у товара "
        for property in Property.objects.all():
            value = property.values.filter(default=True)[0] \
                if property.values.filter(default=True) and not property.optional else None
            if not kwargs['object'].product_parameters.filter(property=property):
                kwargs['object'].product_parameters.create(
                    property=property,
                    value=value
                )
            if not kwargs['object'].product_add_parameters.filter(property=property):
                " Создать доп параметры товара "
                kwargs['object'].product_add_parameters.create(
                    property=property
                )
    elif isinstance(kwargs['object'], Section):
        " Создание существующих параметров у раздела "
        for property in Property.objects.all():
            value = property.values.filter(default=True)[0] \
                if property.values.filter(default=True) and not property.optional else None
            if not kwargs['object'].section_parameters.filter(property=property):
                kwargs['object'].section_parameters.create(
                    property=property,
                    value=value
                )
            if not kwargs['object'].section_add_parameters.filter(property=property):
                " Создать доп параметры Раздела "
                kwargs['object'].section_add_parameters.create(
                    property=property
                )
    elif isinstance(kwargs['object'], Category):
        " Создание существующих параметров у категории "
        for property in Property.objects.all():
            if not kwargs['object'].category_parameters.filter(property=property):
                value = property.values.filter(default=True)[0]\
                    if property.values.filter(default=True) and not property.optional else None
                kwargs['object'].category_parameters.create(
                    property=property,
                    value=value
                )

value_saved.connect(create_parameter)
object_saved.connect(create_parameter)
parameter_saved.connect(create_parameter)


def set_products_by_parameters(sender, instance, **kwargs):
    """ При изменении параметров, назначить товары по параметрам для категорий """
    for category in Category.objects.all():
        parameters = list(
            category.category_parameters.exclude(value=None).values_list('value', flat=True).order_by('value')
        )
        product_ids = [
            product.id for product in Product.objects.all() if
            all(val in parameters for val in list(product.get_parameters().values_list('value', flat=True)))
        ]
        category.products_by_parameters.set(Product.objects.filter(id__in=product_ids))
        category.save()
# post_save.connect(set_products_by_parameters, sender=Parameter)