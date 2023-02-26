# -*- coding: utf-8 -*-
from os.path import join
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from pages import settings
from pages.admin import PageAdmin
from pages.models import Page, PageAlias, Media
from ei60doors.custom_pages.models import Advantage, CatalogItem
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


class CatalogItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CatalogItem


class CustomPageAdmin(PageAdmin):

    class Media:

        """ Добавлены кастомные js и сss """

        css = {
            'all': [
                join(settings.PAGES_STATIC_URL, 'css/rte.css'),
                join(settings.PAGES_STATIC_URL, 'css/pages.css'),
                'css/admin/custom_pages.css',  # Доработка change form стилей
                'css/admin/common.css'  # Добавление глобальных стилей
            ]
        }
        js = [
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.rte.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages_list.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/pages_form.js'),
            'js/admin/pages_form_extra.js',
            join(settings.PAGES_STATIC_URL, 'javascript/jquery.query-2.1.7.js'),
            join(settings.PAGES_STATIC_URL, 'javascript/iframeResizer.min.js'),
        ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        page = Page.objects.get(pk=object_id)

        # Insert popular items
        catalog_inline_exist = False
        page_templates = ['pages/frontpage.html', ]
        for inline in self.inlines:
            if inline is CatalogItemInline:
                catalog_inline_exist = True
                if not page.template in page_templates:
                    self.inlines.remove(inline)

        if not catalog_inline_exist and page.template in page_templates:
            self.inlines.insert(0, CatalogItemInline)

        return super(PageAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

try:
    admin.site.unregister(Media)
    admin.site.unregister(PageAlias)
except NotRegistered:
    pass

try:
    admin.site.unregister(Page)
    admin.site.register(Page, CustomPageAdmin)
except NotRegistered:
    pass

@admin.register(Advantage)
class AdvantageAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
