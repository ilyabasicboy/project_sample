# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import NewsRootAdminForm, NewsAdminForm
from .models import NewsRoot, CustomNews
from easy_news.models import News


@admin.register(NewsRoot)
class NewsRootAdmin(admin.ModelAdmin):

    model = NewsRoot
    form = NewsRootAdminForm

    def has_add_permission(self, request):
        return not bool(NewsRoot.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    def response_post_save_change(self, request, obj):

        """ Редирект на страницу списка новостей после сохранения """

        post_url = reverse('admin:easy_news_news_changelist', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


admin.site.unregister(News)
@admin.register(CustomNews)
class NewsAdmin(admin.ModelAdmin):

    # @property
    # def media(self):
    #     media = super(NewsAdmin, self).media
    #     media.add_css(news_settings.ADMIN_EXTRA_CSS)
    #     return media

    list_filter = ['show']
    search_fields = ['title', 'text', ]
    list_display = ['title', 'date', 'show', ]
    prepopulated_fields = {'slug': ('title',)}
    model = CustomNews
    form = NewsAdminForm


