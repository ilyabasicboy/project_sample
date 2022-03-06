# -*- encoding: utf-8 -*-
from catalog.apps import CustomCatalogBaseConfig


class CustomCatalogAppConfig(CustomCatalogBaseConfig):
    name = 'tordoors_new.custom_catalog'
    verbose_name = u'Модели каталога'

    def ready(self):
        super(CustomCatalogAppConfig, self).ready()
        import tordoors_new.custom_catalog.signals
