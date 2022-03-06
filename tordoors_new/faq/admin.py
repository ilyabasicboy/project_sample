# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site
from .models import FaqQuestion, FaqTheme
from .forms import FaqQuestionAdminForm, FaqThemeForm
from adminsortable2.admin import SortableAdminMixin


class FaqQuestionAdmin(SortableAdminMixin, ModelAdmin):

    def get_answer(self, obj):
        return True if obj.answer else False

    def get_ask(self, obj):
        return obj.question if len(obj.question) < 70 else obj.question[0:70] + '...'

    get_answer.boolean = True
    get_answer.short_description = u'Ответ'
    get_ask.short_description = u'Вопрос'

    model = FaqQuestion
    form = FaqQuestionAdminForm
    ordering = ('order_key', 'theme', 'datetime',)
    list_display = ('get_ask', 'get_answer', 'theme', 'show', 'datetime', )
    list_editable = ('show',)
    list_filter = ('theme', )

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'datetime', 'show',),
        }),
        (None, {
            'fields': ('theme', 'question', 'answer', ),
        }),
    )


class FaqThemeAdmin(SortableAdminMixin, ModelAdmin):
    model = FaqTheme
    form = FaqThemeForm
    prepopulated_fields = {"slug": ("name",)}


site.register(FaqQuestion, FaqQuestionAdmin)
site.register(FaqTheme, FaqThemeAdmin)
