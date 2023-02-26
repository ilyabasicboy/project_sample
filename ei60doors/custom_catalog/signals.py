# -*- encoding: utf-8 -*-
from mptt.signals import node_moved
from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from catalog.models import TreeItem
from ei60doors.custom_catalog.models import Section, Product, Category


def catalog_changed_handler(sender, instance, **kwargs):

    """ Логика очистки кэша после изменения каталога """

    cache.clear()


post_save.connect(catalog_changed_handler, sender=Section)
post_save.connect(catalog_changed_handler, sender=Product)
post_save.connect(catalog_changed_handler, sender=Category)
pre_delete.connect(catalog_changed_handler, sender=Section)
pre_delete.connect(catalog_changed_handler, sender=Product)
pre_delete.connect(catalog_changed_handler, sender=Category)
node_moved.connect(catalog_changed_handler, sender=TreeItem)
