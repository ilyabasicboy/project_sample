# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.mail.message import EmailMessage

from tordoors_new.custom_feedback.forms import BaseForm
from tordoors_new.reviews.models import Review
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError



def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(u"Максимальный размер файла 5 мб")
    else:
        return value


class ReviewForm(forms.ModelForm, BaseForm):

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

    image = forms.FileField(
        label=u'Прикрепить файл к сообщению',
        validators=[validate_file_size],
        required=False, help_text=u'(максимальный размер файла 5 МБ)',
    )

    confirm = forms.BooleanField(
        label=u'Согласие на обработку',
        required=True,
        initial=True
    )


    class Meta:
        model = Review
        exclude = ('date',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Иван Петров'}),
            'content': forms.Textarea(attrs={'placeholder': 'Здравствуйте...'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
        }
        labels = {
            'name': u"Ваше имя, название организации",
            'phone': u'Ваш телефон',
            'email': u'Ваш E-mail',
            'content': u'Текст отзыва',
        }


    subject = settings.EMAIL_SUBJECT_PREFIX + u'Отправить отзыв'

    def clean(self):

        if len(self.cleaned_data.get('message_', '')):
            self._errors['message_'] = 'unhuman message found'
            raise PermissionDenied
        for key, value in self.cleaned_data.items():
            if isinstance(value, str) and ('href=' in value or 'http' in value):
                self._errors['message_'] = 'external links found'
                raise PermissionDenied

        return self.cleaned_data

    def mail(self, request):

        message = self.render_message(request)
        headers = {}
        if 'email' in self.cleaned_data:
            headers = {'Reply-to': self.cleaned_data.get('email')}

        msg = EmailMessage(self.subject, message, self.sender, self.recipients, headers=headers)
        if request.FILES:
            uploaded_file = request.FILES['image'] # file is the name value which you have provided in form for file field
            msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        msg.send()
        self.after_mail(message=message, headers=headers)