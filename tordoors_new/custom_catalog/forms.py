# -*- coding: utf-8 -*-
from django import forms
from .models import Root, Product, Property, Parameter, Section, Doc, Value, AddParameter,\
    ProductImage, Category, FireResistance, Facing, FacingPrint, FacingColor
from attachment.settings import ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE
from attachment.widgets import ImagePreviewWidget
from attachment.forms import validate_size
from django.contrib.admin.widgets import FilteredSelectMultiple


class RootAdminForm(forms.ModelForm):

    class Meta:
        model = Root
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'long_title': forms.TextInput(attrs={'class': 'large-input'}),
        }


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
            'add_options': FilteredSelectMultiple(verbose_name=u'Доп. опции', is_stacked=False)
        }


class SectionAdminForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
            'articles': FilteredSelectMultiple(verbose_name=u'Статьи', is_stacked=False),
            'add_options': FilteredSelectMultiple(verbose_name=u'Доп. опции', is_stacked=False)
        }


class FacingPrintAdminForm(forms.ModelForm):

    class Meta:
        model = FacingPrint
        fields = '__all__'
        widgets = {
            'facing': FilteredSelectMultiple(verbose_name=u'Типы отделки', is_stacked=False),
        }


class FacingColorAdminForm(forms.ModelForm):

    class Meta:
        model = FacingColor
        exclude = ('order_key',)
        widgets = {
            'facing': FilteredSelectMultiple(verbose_name=u'Типы отделки', is_stacked=False),
        }


class DocAdminForm(forms.ModelForm):

    class Meta:
        model = Doc
        fields = '__all__'
        widgets = {'item_types': FilteredSelectMultiple(verbose_name=u'Виды изделий', is_stacked=False)}


class ParameterAdminForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = ['property', 'value']

    def __init__(self, *args, **kwargs):
        super(ParameterAdminForm, self).__init__(*args, **kwargs)

        """Ограничить количество вариантов значений в зависимости от выбранного параметра в форме"""
        if 'property' in self.initial:
            CHOICES = ((None, '--------'),)
            CHOICES += tuple((value.id, value.name) for value in Value.objects.filter(property=self.initial['property']))
            self.fields['value'].choices = CHOICES
            property = Property.objects.get(id=self.initial['property'])
            self.fields['property'].choices = [(property.id, property.name)]


class AddParameterAdminForm(forms.ModelForm):
    class Meta:
        model = AddParameter
        fields = ['property', 'values']


    def __init__(self, *args, **kwargs):
        super(AddParameterAdminForm, self).__init__(*args, **kwargs)

        """Ограничить количество вариантов значений в зависимости от выбранного параметра в форме"""
        if 'property' in self.initial:
            CHOICES = tuple((value.id, value.option_name if value.option_name else value.name) for value in Value.objects.filter(property=self.initial['property']))
            self.fields['values'].choices = CHOICES
            property = Property.objects.get(id=self.initial['property'])
            self.fields['property'].choices = [(property.id, property.name)]


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        exclude = ('section', 'product')
        widgets = {
            'image': ImagePreviewWidget,
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        return validate_size(image, ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE)


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {
            'products': FilteredSelectMultiple(verbose_name=u'Товары', is_stacked=False),
            'articles': FilteredSelectMultiple(verbose_name=u'Виды изделий', is_stacked=False)
        }
        exclude = ['products_by_parameters']


class FilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        """ Создание полей динамических параметров для формы """
        """ Try необходим для инициализации миграций в новую бд """
        try:
            for property in Property.objects.filter(show_on_filter=True).order_by('order_key'):
                values = Value.objects.filter(property=property)
                if values:
                    CHOICES = (('', 'Не важно'),)
                    CHOICES += tuple((value.id, value.name) for value in Value.objects.filter(property=property))
                    self.fields[property.slug] = forms.ChoiceField(
                        label=property.name,
                        choices=CHOICES,
                        required=False,
                        widget=forms.Select(attrs={
                            'data-type': 'dynamic',
                        })
                    )
        except:
            pass

    min_price = forms.IntegerField(
        label="Минимальная цена",
        min_value=0,
        widget=forms.HiddenInput
    )
    max_price = forms.IntegerField(
        label="Максимальная цена",
        min_value=0,
        widget=forms.HiddenInput
    )

    dir = forms.ChoiceField(
        label="Сортировка",
        choices=(
            ('new', "Сначала новинки"),
            ('asc', "Сначала недорогие"),
            ('desc', "Сначала дорогие"),
        ),
        initial='new'
    )
    """ Try необходим для инициализации миграций в новую бд """
    try:
        FIRE_CHOICES = tuple(
            (fire.id, fire.name) for fire in FireResistance.objects.all().order_by('order_key')
        )
    except:
        FIRE_CHOICES = None
    if FIRE_CHOICES:
        fireproof = forms.ChoiceField(
            label="Огнестойкость",
            choices=(
                        ('', 'Не важно'),
                        ('0', 'Нет'),
                    ) + FIRE_CHOICES,
            required=False,
            initial='',
            widget = forms.Select(attrs={
                'data-type': 'simple',
            })
        )

    try:
        FACING_CHOICES = tuple(
            (facing.id, facing.name) for facing in Facing.objects.all()
        )
    except:
        FACING_CHOICES = None
    if FACING_CHOICES:
        facing = forms.ChoiceField(
            label="Отделка",
            choices=(('', 'Не важно'),) + FACING_CHOICES,
            widget=forms.Select(attrs={
                'data-type': 'simple',
            })
        )

    def get_dynamic_fields(self):
        """ Returns fields with data-type attr equal to dynamic"""
        return [field for field in self if 'data-type' in field.field.widget.attrs\
                and field.field.widget.attrs['data-type'] == 'dynamic']

    def get_simple_fields(self):
        """ Returns fields with data-type attr equal to simple"""
        return [field for field in self if 'data-type' in field.field.widget.attrs\
                and field.field.widget.attrs['data-type'] == 'simple']