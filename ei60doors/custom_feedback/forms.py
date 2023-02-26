# -*- coding: utf-8 -*-
from django import forms
from django.core.mail.message import EmailMessage
from feedback.forms import BaseFeedbackForm
from django.core.exceptions import ValidationError


def validate_is_human(value):
    if value != 'on':
        raise forms.ValidationError(':(')
    return value


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(u"Максимальный размер файла 5 мб")
    else:
        return value


class BaseForm(BaseFeedbackForm):

    ERROR_MESSAGES = {
        'required': u'Заполните поле',
        'invalid': u'Неправильное значение'
    }

    confirm = forms.BooleanField(
        label=u'Согласие на обработку',
        required=True,
        initial=True
    )

    flag = forms.CharField(
        label=u'Флаг',
        required=False,
        widget=forms.widgets.HiddenInput,
        initial='none',
        validators=[validate_is_human],
    )

    def after_mail(self, **kwargs):

        """ Дополнительная логика после отправки письма
            данные данные формы доступны через self """
        pass

    def __init__(self, *args, **kwargs):

        """ Указание начальных данных формы, например переопределит тексты ошибок """

        super(BaseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].error_messages = self.ERROR_MESSAGES


class MeteringCall(BaseForm):

    """
        Запросить расчет
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )

    file = forms.FileField(
        label=u'Прикрепить файл',
        validators=[validate_file_size],
        required=False,
        help_text=u'Допустимый для загрузки формат: JPG, PNG, PDF, до 5 Мб',
        widget=forms.FileInput(
            attrs={
                'data-accept-imgfile':''
            }
        )
    )

    message = forms.CharField(
        label=u'Ваше сообщение:',
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
            }
        ),
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


class FeedbackCall(BaseForm):

    """
        Обратный звонок
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )


class Order(BaseForm):

    """
        Оформить предзаказ
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )
    message = forms.CharField(
        label=u'Ваше сообщение:',
        max_length=1000,
        required=False,
        widget=forms.TextInput(
            attrs={
            }
        ),
    )


class CallRackman(BaseForm):

    """
        Вызвать замерщика
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )
    date_call = forms.DateTimeField(
        label=u'Желаемая дата замера:*',
    )
    time_call = forms.TimeField(
        label=u'Желаемое время замера:',
        required=False,
        widget=forms.TimeInput(
            attrs={
                'placeholder': 'Желаемое время замера'
            }
        ),
    )


class WantSimilar(BaseForm):

    """
        Интересует похожее изделие
    """

    image_url = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )
    message = forms.CharField(
        label=u'Ваше сообщение:',
        max_length=1000,
        required=False,
        widget=forms.TextInput(
            attrs={
            }
        ),
    )


class Consult(BaseForm):

    """
        Получить консультацию
    """

    name = forms.CharField(
        label=u'Ваше имя:*',
        widget=forms.TextInput(
            attrs={

            }
        ),
    )
    phone = forms.CharField(
        label=u'Ваш телефон:*',
        widget=forms.TextInput(
            attrs={
                'placeholder':'+7 (___) ___-__-__',
            }
        ),
    )
