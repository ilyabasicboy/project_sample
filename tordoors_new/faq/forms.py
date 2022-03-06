# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import PermissionDenied
from feedback.forms import BaseFeedbackForm

from .models import FaqQuestion, FaqTheme
from django.conf import settings
from tordoors_new.custom_feedback.forms import BaseForm


class FaqQuestionAdminForm(forms.ModelForm):

    class Meta:
        model = FaqQuestion
        fields = '__all__'
        widgets = {
            'question': forms.widgets.Textarea(attrs={'rows': 4, 'cols': 100, 'placeholder': u'Опишите проблему, с которой вы столкнулись'}),
            'name': forms.widgets.TextInput(attrs={'placeholder': u'Представьтесь'}),
            'email': forms.widgets.EmailInput(attrs={'placeholder': u'Для связи со специалистом техподдержки'}),
        }

try:
    THEME_CHOICES = ((theme.id, theme.name) for theme in FaqTheme.objects.all())
except:
    THEME_CHOICES = ()

class FaqQuestionForm(forms.ModelForm, BaseForm):

    class Meta:
        model = FaqQuestion
        exclude = ('order_key', 'datetime',)
        widgets = {'answer': forms.widgets.Textarea(),
                   'question': forms.widgets.Textarea(attrs={'placeholder': u'Уточните пожалуйста'}),
                   'name': forms.widgets.TextInput(attrs={'placeholder': u'Иван Петров'}),
                   'email': forms.widgets.EmailInput(attrs={'placeholder': u'i.petrov@site.ru'}),
                  }
        labels = {
            'theme': u"Тема вопроса",
            'email': u'Ваш E-mail',
        }

    # Скрытое поле для защиты от спам-ботов
    message_ = forms.CharField(
        label=u'Сообщение', required=False,
        widget=forms.Textarea(attrs={'style':
                                         'opacity: 0;'
                                         'width:0;'
                                         'height:0;'
                                         'padding:0;'
                                         'margin:0;'
                                         'border:0;'
                                     })
    )

    phone = forms.CharField(
        label=u'Ваш телефон',
        required=False,
        widget=forms.TextInput(attrs={'placeholder':'+7 (___) ___-__-__'}),
    )

    confirm = forms.BooleanField(
        label=u'Согласие на обработку',
        required=True,
        initial=True
    )


    subject = settings.EMAIL_SUBJECT_PREFIX + u'FAQ'


    def clean(self):

        if len(self.cleaned_data.get('message_', '')):
            self._errors['message_'] = 'unhuman message found'
            raise PermissionDenied
        for key, value in self.cleaned_data.items():
            if isinstance(value, str) and ('href=' in value or 'http' in value):
                self._errors['message_'] = 'external links found'
                raise PermissionDenied

        return self.cleaned_data


class FaqThemeForm(forms.ModelForm):
    class Meta:
        model = FaqTheme
        fields = '__all__'
        widgets = {'slug': forms.widgets.HiddenInput(),}

