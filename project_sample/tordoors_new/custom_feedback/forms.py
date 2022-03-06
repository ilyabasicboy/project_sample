# -*- coding: utf-8 -*-
from django import forms
from django.core.mail.message import EmailMessage
from feedback.forms import BaseFeedbackForm
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(u"Максимальный размер файла 5 мб")
    else:
        return value

class BaseForm(BaseFeedbackForm):
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

    confirm = forms.BooleanField(
        label=u'Согласие на обработку',
        required=True,
        initial=True
    )

    ERROR_MESSAGES = {
        'required': u'Заполните поле',
        'invalid': u'Неправильное значение'
    }

    def after_mail(self, **kwargs):

        """ Дополнительная логика после отправки письма
            данные данные формы доступны через self """
        pass

    def __init__(self, *args, **kwargs):

        """ Указание начальных данных формы, например переопределит тексты ошибок """

        super(BaseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].error_messages = self.ERROR_MESSAGES

    def clean(self):
        if len(self.cleaned_data.get('message_', '')):
            self._errors['message_'] = 'unhuman message found'
            raise PermissionDenied
        for key, value in self.cleaned_data.items():
            if isinstance(value, str) and ('href=' in value or 'http' in value):
                self._errors['message_'] = 'external links found'
                raise PermissionDenied

        return self.cleaned_data


class MeteringCall(BaseForm):

    """ Записаться на замер """

    name = forms.CharField(
        label=u'Ваше имя',
        widget=forms.TextInput(attrs={
                                    'data-set': 1,
                                    'placeholder':'Иван Петров'
                                      }),
    )

    phone = forms.CharField(
        label=u'Контактный телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )


class DirectorMailForm(BaseForm):

    """ Письмо директору """

    theme = forms.CharField(
        label=u'Тема обращения',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 2,
            'placeholder': 'Возможность сотрудничества',
        }),
    )

    message = forms.CharField(
        label=u'Ваше сообщение:', max_length=1000,
        widget=forms.Textarea(attrs={
            'data-set': 2,
            'placeholder': 'Здравствуйте...',
        }),
    )

    name = forms.CharField(
        label=u'Ваше имя',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'Иван Петров',
        }),
    )

    phone = forms.CharField(
        label=u'Ваш телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )

    email = forms.EmailField(
        label=u'Ваш E-mail',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'i.petrov@site.ru',
        }),
    )


class CommercialForm(BaseForm):

    """ Заявка на коммерческое предложение """

    name = forms.CharField(
        label=u'Ваше имя',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'Иван Петров',
        }),
    )

    phone = forms.CharField(
        label=u'Ваш телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )

    email = forms.EmailField(
        label=u'Ваш E-mail',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'i.petrov@site.ru',
        }),
    )

    comment = forms.CharField(
        label=u'Комментарий для менеджера:', max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'data-set': 2,
            'placeholder': 'Жду коммерческое предложение',
        }),
    )

    file = forms.FileField(
        label=u'Прикрепить файл к сообщению',
        validators=[validate_file_size],
        required=False, help_text=u'(максимальный размер файла 5 МБ)',
    )

    def mail(self, request):

        message = self.render_message(request)
        headers = {}
        if 'email' in self.cleaned_data:
            headers = {'Reply-to': self.cleaned_data.get('email')}

        msg = EmailMessage(self.subject, message, self.sender, self.recipients, headers=headers)
        if request.FILES:
            uploaded_file = request.FILES['file'] # file is the name value which you have provided in form for file field
            msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        msg.send()
        self.after_mail(message=message, headers=headers)


class CalculateForm(BaseForm):

    """ Заявка на индивидуальный расчет """

    name = forms.CharField(
        label=u'Ваше имя',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'Иван Петров',
        }),
    )

    phone = forms.CharField(
        label=u'Ваш телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )

    email = forms.EmailField(
        label=u'Ваш E-mail',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'i.petrov@site.ru',
        }),
    )

    comment = forms.CharField(
        label=u'Комментарий для менеджера:', max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'data-set': 2,
            'placeholder': 'Жду коммерческое предложение',
        }),
    )

    file = forms.FileField(
        label=u'Прикрепить файл к сообщению',
        validators=[validate_file_size],
        required=False, help_text=u'(максимальный размер файла 5 МБ)',
    )

    def mail(self, request):

        message = self.render_message(request)
        headers = {}
        if 'email' in self.cleaned_data:
            headers = {'Reply-to': self.cleaned_data.get('email')}

        msg = EmailMessage(self.subject, message, self.sender, self.recipients, headers=headers)
        if request.FILES:
            uploaded_file = request.FILES['file'] # file is the name value which you have provided in form for file field
            msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        msg.send()
        self.after_mail(message=message, headers=headers)


class Order(BaseForm):
    """ Оформить заявку """

    popup_text = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(
        label=u'Ваше имя',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'Иван Петров',
        }),
    )

    phone = forms.CharField(
        label=u'Ваш телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )

    email = forms.EmailField(
        label=u'Ваш E-mail',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'i.petrov@site.ru',
        }),
    )

    comment = forms.CharField(
        label=u'Комментарий для менеджера:', max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'data-set': 2,
            'placeholder': 'Адрес места монтажа',
        }),
    )


class OrderDelivery(BaseForm):
    """ Заказать на странице доставки """

    name = forms.CharField(
        label=u'Ваше имя',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'Иван Петров',
        }),
    )

    phone = forms.CharField(
        label=u'Ваш телефон:',
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': '+7 (___) ___-__-__',
        }),
    )

    email = forms.EmailField(
        label=u'Ваш E-mail',
        required=False,
        widget=forms.TextInput(attrs={
            'data-set': 1,
            'placeholder': 'i.petrov@site.ru',
        }),
    )