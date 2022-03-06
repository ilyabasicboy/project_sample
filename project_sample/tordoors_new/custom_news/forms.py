# -*- coding: utf-8 -*-
from django import forms
from .models import NewsRoot, CustomNews
from easy_news import settings as news_settings
from easy_news.forms import get_extra_class


class NewsRootAdminForm(forms.ModelForm):
    class Meta:
        model = NewsRoot
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
        }


class NewsAdminForm(forms.ModelForm):

    class Meta:
        model = CustomNews
        fields = 'show', 'title', 'slug', 'date', 'text', 'video'
        widgets = {
            'title': forms.TextInput(attrs={'class': get_extra_class('title')}),
            'author': forms.TextInput(attrs={'class': get_extra_class('author')}),
            'slug': forms.TextInput(attrs={'class': get_extra_class('slug')})
        }

    if news_settings.NEWS_TAGGING:
        tags = TagField(required=False)