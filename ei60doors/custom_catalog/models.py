# -*- encoding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from tinymce.models import HTMLField
from catalog.models import CatalogBase
from catalog.utils import get_content_objects, get_sorted_content_objects
from pages.models import Page
from django.core.cache import cache
from django.db.models import Max, Min


CONSTRUCTION_CHOICES = (
    (0, 'Однопольная'),
    (1, 'Полуторапольная'),
    (2, 'Двупольная'),
)

FIREPROOF_CHOICES = (
    (0, 'Ei-30'),
    (1, 'Ei-60'),
    (2, 'Ei-90'),
)

GROUP_CHOICES = (
    (1, 'Двери по назначению'),
    (2, 'Двери по наружной отделке'),
    (3, 'Двери по особенностям')
)

SORT_CHOICES = (
    ('asc', "Сначала дешевые"),
    ('desc', "Сначала дорогие"),
    ('new', "Новинки сверху"),
)


class CatalogMixin:

    def get_products_count(self):
        result = cache.get(self.cache_key()+'_products_count', None)
        if not result:
            result = self.get_products().count()
            cache.set(self.cache_key()+'_products_count', result, 600000)
        return result

    def cache_key(self):
        return '%s_%d' % (self.__class__.__name__, self.id)

    def get_min_price(self):

        result = cache.get(self.cache_key()+'_min_price', 0)
        if not result:
            prices = self.get_products().aggregate(Min('price'))
            result = prices['price__min']
            cache.set(self.cache_key()+'_min_price', result, 600000)
        return result

    def get_max_price(self):
        result = cache.get(self.cache_key()+'_max_price', 0)
        if not result:
            prices = self.get_products().aggregate(Max('price'))
            result = prices['price__max']
            cache.set(self.cache_key()+'_max_price', result, 600000)
        return result


class Root(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'корневая страница'
        verbose_name_plural = verbose_name

    slug = ''
    title = models.CharField(
        verbose_name=u'название',
        max_length=400
    )
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        blank=True, null=True
    )
    sort = models.CharField(
        verbose_name=u'Сортировать товары',
        default='new',
        choices=SORT_CHOICES,
        max_length=255
    )

    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self, *args, **kwargs):
        return u'Корневая страница'

    def get_absolute_url(self):
        return reverse('catalog-root')

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = Product.objects.filter(show=True).order_by('-id')
            if self.sort == 'asc':
                result = result.order_by('price')
            elif self.sort == 'desc':
                result = result.order_by('-price')
            else:
                result = result.order_by('-id')
            cache.set(self.cache_key() + '_products', result, 600000)
        return result


class Product(CatalogBase):

    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'

    leaf = True
    title = models.CharField(
        verbose_name=u'название',
        max_length=400
    )
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        null=True,
        blank=True
    )
    google_prefix = models.CharField(
        verbose_name=u'Префикс Google Merchant',
        max_length=400,
        blank=True, null=True,
        help_text=u'Добавляет префикс к длинному названию товара в google merchant'
    )
    exclude_google_merchant = models.BooleanField(
        verbose_name=u'Не выгружать в Google Merchant',
        default=False
    )
    exclude_direct_yml = models.BooleanField(
        verbose_name=u'Не выгружать в Yandex Директ',
        default=False,
    )
    price = models.PositiveIntegerField(
        verbose_name=u'цена',
        default=0
    )
    old_price = models.PositiveIntegerField(
        verbose_name=u'старая цена',
        default=0
    )
    habarytes = models.TextField(
        verbose_name=u'Габариты',
        max_length=255,
        blank=True,
        null=True
    )
    construction = models.IntegerField(
        verbose_name=u'Конструкция',
        choices=CONSTRUCTION_CHOICES,
        blank=True,
        null=True
    )
    fireproof = models.IntegerField(
        verbose_name=u'Огнестойкость',
        choices=FIREPROOF_CHOICES,
        blank=True,
        null=True
    )
    readiness = models.CharField(
        verbose_name=u'Готовность',
        max_length=255,
        blank=True,
        null=True
    )
    delivery = models.CharField(
        verbose_name=u'Доставка',
        max_length=255,
        blank=True,
        null=True,
    )
    mounting = models.CharField(
        verbose_name=u'монтаж',
        max_length=500,
        blank=True,
        null=True
    )
    specs = HTMLField(
        verbose_name=u'Характеристики',
        blank=True,
        null=True
    )
    finish = models.ManyToManyField(
        Page,
        verbose_name=u'Варианты отделки',
        related_name='finish_products',
        limit_choices_to={
            'template': 'pages/finish.html',
            'status': Page.PUBLISHED,
        },
        blank=True
    )
    services = HTMLField(
        verbose_name=u'Услуги',
        blank=True,
        null=True
    )
    gallery = models.ForeignKey(
        Page,
        verbose_name=u'Галерея',
        related_name='gallery_products',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'template': 'pages/gallery.html',
            'status': Page.PUBLISHED,
        }
    )

    def __str__(self):
        return '%s - %s' % (self.title, self.id)


class Section(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'раздел'
        verbose_name_plural = u'разделы'

    title = models.CharField(
        verbose_name=u'название',
        max_length=400
    )
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        null=True,
        blank=True
    )
    google_prefix = models.CharField(
        verbose_name=u'Префикс Google Merchant',
        max_length=400,
        blank=True, null=True,
        help_text=u'Добавляет префикс к длинному названию дочерних товаров в google merchant'
    )
    google_merchant = models.BooleanField(
        verbose_name=u'Выгружать в Google Merchant',
        default=True,
        help_text=u'Наследуется в товары'
    )
    sort = models.CharField(
        verbose_name=u'Сортировать товары',
        default='new',
        choices=SORT_CHOICES,
        max_length=255
    )
    group = models.IntegerField(
        verbose_name=u'Группа',
        choices=GROUP_CHOICES,
        blank=True,
        null=True
    )
    habarytes = models.TextField(
        verbose_name=u'Габариты',
        max_length=255,
        blank=True,
        null=True
    )
    construction = models.IntegerField(
        verbose_name=u'Конструкция',
        choices=CONSTRUCTION_CHOICES,
        blank=True,
        null=True
    )
    fireproof = models.IntegerField(
        verbose_name=u'Огнестойкость',
        choices=FIREPROOF_CHOICES,
        blank=True,
        null=True
    )
    readiness = models.CharField(
        verbose_name=u'Готовность',
        max_length=255,
        blank=True,
        null=True
    )
    delivery = models.CharField(
        verbose_name=u'Доставка',
        max_length=255,
        blank=True,
        null=True,
    )
    mounting = models.CharField(
        verbose_name=u'монтаж',
        max_length=500,
        blank=True,
        null=True
    )
    specs = HTMLField(
        verbose_name=u'Характеристики',
        blank=True,
        null=True
    )
    finish = models.ManyToManyField(
        Page,
        verbose_name=u'Варианты отделки',
        related_name='finish_sections',
        limit_choices_to={
            'template': 'pages/finish.html',
            'status': Page.PUBLISHED,
        },
        blank=True
    )
    services = HTMLField(
        verbose_name=u'Услуги',
        blank=True,
        null=True
    )
    gallery = models.ForeignKey(
        Page,
        verbose_name=u'Галерея',
        related_name='gallery_sections',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'template': 'pages/gallery.html',
            'status': Page.PUBLISHED,
        }
    )

    def __str__(self):
        return self.title

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = Product.objects.filter(tree__parent__object_id=self.id, show=True)
            if self.sort == 'asc':
                result = result.order_by('price')
            elif self.sort == 'desc':
                result = result.order_by('-price')
            else:
                result = result.order_by('-id')
            cache.set(self.cache_key() + '_products', result, 600000)
        return result


class Category(CatalogBase, CatalogMixin):
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'

    leaf = True

    title = models.CharField(
        verbose_name=u'название',
        max_length=400
    )
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400
    )
    sort = models.CharField(
        verbose_name=u'Сортировать товары',
        default='new',
        choices=SORT_CHOICES,
        max_length=255
    )
    group = models.IntegerField(
        verbose_name=u'Группа',
        choices=GROUP_CHOICES,
        blank=True,
        null=True
    )
    products = models.ManyToManyField(
        Product,
        verbose_name=u'Товары',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_products(self):
        result = cache.get(self.cache_key() + '_products')
        if result is None:
            result = self.products.filter(show=True)
            if self.sort == 'asc':
                result = result.order_by('price')
            elif self.sort == 'desc':
                result = result.order_by('-price')
            else:
                result = result.order_by('-id')
            cache.set(self.cache_key() + '_products', result, 600000)
        return result
