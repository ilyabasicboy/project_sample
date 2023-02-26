# -*- encoding: utf-8 -*-
from catalog.apps import CustomCatalogBaseConfig


class CustomCatalogAppConfig(CustomCatalogBaseConfig):
    name = 'ei60doors.custom_catalog'
    verbose_name = u'Модели каталога'

    def ready(self):
        super(CustomCatalogAppConfig, self).ready()
        import ei60doors.custom_catalog.signals
