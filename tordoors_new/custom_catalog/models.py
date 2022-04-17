# -*- encoding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from tinymce.models import HTMLField
from catalog.models import CatalogBase
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects
from imagekit.models import ImageModel
from attachment.fields import ImagePreviewField
from attachment.settings import ATTACHMENT_CACHE_DIR, ATTACHMENT_IKSPECS, ATTACHMENT_UPLOAD_DIR
import os
import django.dispatch
from pages.models import Page

value_saved = django.dispatch.Signal()
object_saved = django.dispatch.Signal()
parameter_saved = django.dispatch.Signal()

TYPE_CHOICES = (
    ('двери', 'Двери'),
    ('люки', 'Люки'),
    ('ворота', 'Ворота'),
    ('прочие изделия', 'Прочие изделия'),
)

SIDE_CHOICES = (
    ('inside', 'Внутренняя'),
    ('outside', 'Внешняя')
)

class Root(CatalogBase):
    class Meta:
        verbose_name = u'корневая страница'
        verbose_name_plural = verbose_name

    slug = ''
    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(verbose_name=u'длинное название', max_length=400, blank=True, null=True)
    top_content = HTMLField(verbose_name=u'контент в начале страницы', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент в конце страницы', blank=True, null=True)

    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self, *args, **kwargs):
        return u'Корневая страница'

    def get_absolute_url(self):
        return reverse('catalog-root')

    def get_min_price(self):
        rslt = 0
        prices = Product.objects.filter(show=True).values_list('price', flat=True)
        try:
            rslt = min(prices)
        except:
            pass
        return rslt

    def get_max_price(self):
        prices = Product.objects.filter(show=True).values_list('price', flat=True)
        rslt = 0
        try:
            rslt = max(prices)
        except:
            pass
        return rslt

    def get_products(self):
        return Product.objects.filter(show=True).order_by('tree__id')

    @property
    def root_sections(self):

        """ Возвращает список разделов верхнего уровня"""

        return get_sorted_content_objects(
            get_content_objects(self.tree.get().get_children(), allowed_models=(Section,))
        )


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
        verbose_name=u'Длинное название',
        max_length=400,
        blank=True, null=True
    )
    popular = models.BooleanField(verbose_name='Популярный товар', default=False)
    item_type = models.ForeignKey('ItemType', verbose_name=u'вид изделия', on_delete=models.CASCADE, blank=True,
                                  null=True)
    box_size = models.CharField(verbose_name=u'размер коробки', max_length=400, default='950 x 2050')
    production_time = models.IntegerField(
        verbose_name=u'Срок изготовления', default=12, help_text='часов'
    )
    guarantee = models.IntegerField(
        verbose_name=u'Гарантия на дверь', default=5, help_text='лет'
    )
    show_one_side = models.CharField(
        verbose_name=u'показывать только одну сторону',
        choices=SIDE_CHOICES,
        null=True,
        blank=True,
        max_length=255,
    )
    price = models.PositiveIntegerField(
        verbose_name=u'цена',
        blank=True,
        null=True,
        default=0
    )
    price_per_square = models.BooleanField(
        verbose_name=u'цена за квадратный метр',
        default=False
    )
    facing = models.ForeignKey(
        'Facing',
        verbose_name='Отделка',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = HTMLField(verbose_name=u'описание', default='', blank=True)
    bottom_content = HTMLField(verbose_name=u'контент внизу страницы', default='', blank=True)

    @property
    def images(self):
        " Возвращает список изображений сгруппированный по цветам и сторонам "
        images_list = []
        """
        Если есть инлайны без подгруженного изображения,
        искать такие же записи с изображением в родительских разделах
        """
        empty_images = self.get_side_images()
        images = ProductImage.objects.filter(product=self.id).exclude(image='') \
                 | ProductImage.objects.filter(id__in=empty_images)

        #Colors order must be kept as defined in admin site
        color_ids_all = images.values_list('color', flat=True)
        color_ids = []
        for id in color_ids_all:
            if id not in color_ids:
                color_ids.append(id)

        colors = [FacingColor.objects.get(id=id) for id in color_ids]

        for color in colors:
            images_list.append({
                'color': color,
                'inside': images.filter(color=color.id, side='inside').first(),
                'outside': images.filter(color=color.id, side='outside').first(),
            })
        return images_list

    def get_show_one_side(self):
        result = None
        if self.show_one_side:
            result = self.show_one_side
        else:
            try:
                result = self.tree.get().parent.content_object.get_show_one_side()
            except:
                pass
        return result

    def get_parameters(self):
        """ Возвращает список параметров наследуемых от родительских разделов """
        all_parameters = self.product_parameters.all()
        empty_parameters = all_parameters.filter(value=None)
        parameters = all_parameters.exclude(id__in=empty_parameters.values_list('id', flat=True))
        if empty_parameters:
            try:
                parent_parameters = self.tree.get().parent.content_object.get_parameters(
                    empty_parameters.values_list('property', flat=True))
            except:
                parent_parameters = None
            if parent_parameters:
                parameters = parameters | parent_parameters
        return parameters

    def get_add_parameters(self):
        """ Возвращает список доп. параметров наследуемых от родительских разделов """
        all_parameters = self.product_add_parameters.all()
        empty_parameters = all_parameters.filter(values=None)
        parameters = all_parameters.exclude(id__in=empty_parameters.values_list('id', flat=True))
        if empty_parameters and self.tree.get().parent:
            try:
                parent_parameters = self.tree.get().parent.content_object.get_add_parameters(
                    empty_parameters.values_list('property', flat=True))
            except:
                parent_parameters = None
            if parent_parameters:
                parameters = parameters | parent_parameters
        return parameters

    def get_product_type(self):
        """ Найти тип изделия рекурсией(у родительских разделов) """
        rslt = ''
        try:
            rslt = self.tree.get().parent.content_object.get_product_type()
        except:
            pass
        return rslt

    def get_side_images(self):
        """ Найти изображения сторон рекурсией(у родительских разделов) """
        result = []
        empty_images = ProductImage.objects.filter(product=self.id, image='')
        if empty_images:
            for image in empty_images:
                try:
                    parent = self.tree.get().parent.content_object
                    result.append(
                        parent.get_side_images(image.side, self.facing, image.color, image.print)
                    )
                except:
                    pass
        return result

    def get_item_type(self):
        """ Найти вид изделия рекурсией(у родительских разделов) """
        result = None
        if self.item_type:
            result = self.item_type
        else:
            try:
                result = self.tree.get().parent.content_object.get_item_type()
            except:
                pass
        return result

    def get_delivery_moscow(self):
        result = None
        try:
            result = self.tree.get().parent.content_object.get_delivery_moscow()
        except:
            pass
        return result

    def get_delivery_russia(self):
        result = None
        try:
            result = self.tree.get().parent.content_object.get_delivery_russia()
        except:
            pass
        return result

    def get_installation(self):
        result = None
        try:
            result = self.tree.get().parent.content_object.get_installation()
        except:
            pass
        return result

    def get_service(self):
        result = None
        try:
            result = self.tree.get().parent.content_object.get_service()
        except:
            pass
        return result

    def __str__(self):
        return self.title if self.title else self.slug

    def full_path(self):
        """
        Get url path ancestors
        """
        path = []
        for ancestor in self.tree.get().get_ancestors(ascending=False):
            if ancestor.content_object.slug:
                path.append(ancestor.content_object.slug)
        if self.slug:
            path.append(self.slug)
        return '/'.join(path)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        object_saved.send(sender=self.__class__, object=self)


class ProductImage(ImageModel):
    class Meta:
        verbose_name = 'Изображение товара с отделкой'
        verbose_name_plural = 'Изображения товара с отделкой'
        ordering = ('order_key', 'facing')

    class IKOptions:
        spec_module = ATTACHMENT_IKSPECS
        cache_dir = ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    product = models.ForeignKey(
        Product,
        related_name='product_attachment_image_id',
        verbose_name=u'товар', on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        'Section',
        related_name='section_attachment_image_id',
        verbose_name=u'раздел', on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = ImagePreviewField(
        verbose_name=u'Изображение',
        upload_to=ATTACHMENT_UPLOAD_DIR,
        null=True,
        blank=True
    )
    side = models.CharField(
        verbose_name=u'Сторона двери',
        choices=SIDE_CHOICES,
        max_length=255,
        default='inside',
    )
    facing = models.ForeignKey(
        'Facing',
        related_name='product_facing_id',
        verbose_name=u'Отделка', on_delete=models.CASCADE,
        blank=True, null=True
    )
    color = models.ForeignKey(
        'FacingColor',
        related_name='product_color_id',
        verbose_name=u'Цвет отделки', on_delete=models.CASCADE,
        blank=True, null=True
    )
    print = models.ForeignKey(
        'FacingPrint',
        related_name='product_print_id',
        verbose_name=u'Рисунок отделки', on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        if self.image:
            return os.path.basename(self.image.url)
        else:
            return u''


class Section(CatalogBase):
    class Meta:
        verbose_name = u'раздел'
        verbose_name_plural = u'разделы'

    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(
        verbose_name=u'длинное название',
        max_length=400,
        blank=True, null=True
    )
    show_in_we_produce = models.BooleanField(
        verbose_name=u'отображать в "Мы производим"',
        default=False
    )
    show_in_our_technologies = models.BooleanField(verbose_name=u'отображать в "Наши технологии"', default=False)
    bottom_content = HTMLField(verbose_name=u'контент после списка товаров', blank=True, null=True)
    door_samples = models.ForeignKey(
        Page,
        limit_choices_to={
            'template': 'pages/gallery.html',
        },
        on_delete=models.CASCADE,
        related_name='section_door_samples',
        verbose_name=u'примеры дверей',
        blank=True,
        null=True
    )
    show_one_side = models.CharField(
        verbose_name=u'показывать только одну сторону',
        choices=SIDE_CHOICES,
        null=True,
        blank=True,
        max_length=255,
    )
    item_type = models.ForeignKey(
        'ItemType',
        verbose_name=u'вид изделия',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product_type = models.CharField(
        verbose_name='тип изделия',
        max_length=255,
        choices=TYPE_CHOICES,
        blank=True,
        null=True
    )
    articles = models.ManyToManyField(
        Page,
        limit_choices_to={'template': 'pages/article.html'},
        related_name='section_articles',
        verbose_name=u'Статьи',
        blank=True
    )

    delivery_moscow = HTMLField(verbose_name=u'доставка по Москве и Московской области', blank=True, null=True,)
    delivery_russia = HTMLField(verbose_name=u'Доставка по России', blank=True, null=True,)
    installation = HTMLField(verbose_name=u'установка', blank=True, null=True)
    service = HTMLField(verbose_name=u'гарантийное обслуживание', blank=True, null=True)
    production_time = models.IntegerField(
        verbose_name=u'Срок изготовления', default=12, help_text='часов'
    )
    guarantee = models.IntegerField(
        verbose_name=u'Гарантия на дверь', default=5, help_text='лет'
    )
    fireproof_types = HTMLField(verbose_name=u'Пределы огнестойкости', max_length=400, blank=True, null=True, )
    comment = HTMLField(verbose_name=u'Комментарий', max_length=400, blank=True, null=True, )

    def get_show_one_side(self):
        result = None
        if self.show_one_side:
            result = self.show_one_side
        else:
            try:
                result = self.tree.get().parent.content_object.get_show_one_side()
            except:
                pass
        return result

    def get_item_type(self):
        result = None
        if self.item_type:
            result = self.item_type
        else:
            try:
                result = self.tree.get().parent.content_object.get_item_type()
            except:
                pass
        return result

    def get_side_images(self, side, facing, color, image_print):
        rslt = None
        side_images = self.section_attachment_image_id.filter(
            side=side,
            facing=facing,
            color=color,
            print=image_print
        ).exclude(image='')
        if side_images:
            rslt = side_images[0].id
        elif self.tree.get().parent:
            try:
                rslt = self.tree.get().parent.content_object.get_side_images(side, facing, color, image_print)
            except:
                pass
        return rslt

    def get_delivery_moscow(self):
        result = None
        if self.delivery_moscow:
            result = self.delivery_moscow
        try:
            result = self.tree.get().parent.content_object.get_delivery_moscow()
        except:
            pass
        return result

    def get_delivery_russia(self):
        result = None
        if self.delivery_russia:
            result = self.delivery_russia
        try:
            result = self.tree.get().parent.content_object.get_delivery_russia()
        except:
            pass
        return result

    def get_installation(self):
        result = None
        if self.installation:
            result = self.installation
        try:
            result = self.tree.get().parent.content_object.get_installation()
        except:
            pass
        return result

    def get_service(self):
        result = None
        if self.service:
            result = self.service
        try:
            result = self.tree.get().parent.content_object.get_service()
        except:
            pass
        return result

    def get_parameters(self, empty_parameters):
        parameters = self.section_parameters.filter(property__in=empty_parameters).exclude(value=None)
        empty_parameters = empty_parameters.exclude(property__in=parameters.values_list('property', flat=True))
        if empty_parameters:
            try:
                parent_parameters = self.tree.get().parent.content_object.get_parameters(
                    empty_parameters.values_list('property', flat=True))
            except:
                parent_parameters = None

            if parent_parameters:
                parameters = parameters | parent_parameters
        return parameters

    def get_add_parameters(self, empty_parameters):
        parameters = self.section_add_parameters.filter(property__in=empty_parameters).exclude(values=None)
        empty_parameters = empty_parameters.exclude(property__in=parameters.values_list('property', flat=True))
        if empty_parameters and self.tree.get().parent:
            try:
                parent_parameters = self.tree.get().parent.content_object.get_add_parameters(
                    empty_parameters.values_list('property', flat=True))
            except:
                parent_parameters = None

            if parent_parameters:
                parameters = parameters | parent_parameters
        return parameters

    def get_product_type(self):
        rslt = ''
        if self.product_type:
            rslt = self.product_type
        else:
            try:
                rslt = self.tree.get().parent.content_object.get_product_type()
            except:
                pass
        return rslt

    def get_min_price(self):
        treeitem = self.tree.get()
        children = treeitem.get_descendants().filter(content_type__model='product')
        prices = []
        rslt = 0
        if children:
            for child in children:
                if isinstance(child.content_object, Product):
                    prices.append(child.content_object.price)
        try:
            rslt = min(prices)
        except:
            pass
        return rslt

    def get_max_price(self):
        treeitem = self.tree.get()
        children = treeitem.get_descendants().filter(content_type__model='product')
        prices = []
        rslt = 0
        if children:
            for child in children:
                if isinstance(child.content_object, Product):
                    prices.append(child.content_object.price)
        try:
            rslt = max(prices)
        except:
            pass
        return rslt

    def get_products(self):
        product_ids = self.tree.get().get_descendants().filter(
                content_type__model='product',
            ).order_by('id').values_list('object_id')
        return Product.objects.filter(id__in=product_ids, show=True)

    def get_products_count(self):
        return self.get_products().count()

    def get_fireproof_types(self):
        products = self.get_products()
        item_types = list(set(
                [
                prod.get_item_type().fire_resistance.name for prod in products\
                if prod.get_item_type() and prod.get_item_type().fire_resistance
            ]
        ))
        return item_types

    def save(self, *args, **kwargs):
        super(Section, self).save(*args, **kwargs)
        object_saved.send(sender=self.__class__, object=self)

    def full_path(self):
        """
        Get url path ancestors
        """
        path = []
        for ancestor in self.tree.get().get_ancestors(ascending=False):
            if ancestor.content_object.slug:
                path.append(ancestor.content_object.slug)
        if self.slug:
            path.append(self.slug)
        return '/'.join(path)

    def __str__(self):
        return self.title


class Category(CatalogBase):
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'

    leaf = True
    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(verbose_name=u'длинное название', max_length=400, blank=True, null=True)
    show_in_our_technologies = models.BooleanField(verbose_name=u'отображать в "Наши технологии"', default=False)
    products = models.ManyToManyField(
        Product,
        verbose_name='товары',
        related_name='categories',
        blank=True,
    )
    products_by_parameters = models.ManyToManyField(
        Product,
        help_text=u'Скрытый список',
        verbose_name='товары по параметрам',
        related_name='categories_by_parameters',
        blank=True,
    )
    product_type = models.CharField(
        verbose_name='тип изделия',
        max_length=255,
        choices=TYPE_CHOICES,
        blank=True,
        null=True
    )
    articles = models.ManyToManyField(
        Page,
        limit_choices_to={
            'template': 'pages/article.html',
        },
        related_name='category_articles',
        verbose_name=u'Статьи',
        blank=True
    )
    main_content = HTMLField(verbose_name=u'блок контента', blank=True, null=True)
    door_samples = models.ForeignKey(
        Page,
        limit_choices_to={
            'template': 'pages/gallery.html',
        },
        on_delete=models.CASCADE,
        related_name='category_door_samples',
        verbose_name=u'примеры дверей',
        blank=True,
        null=True
    )
    comment = HTMLField(verbose_name=u'Комментарий', max_length=400, blank=True, null=True, )

    def get_min_price(self):
        rslt = 0
        if self.get_products():
            prices = self.get_products().values_list('price', flat=True)
        try:
            rslt = min(prices)
        except:
            pass
        return rslt

    def get_max_price(self):
        rslt = 0
        if self.get_products():
            prices = self.get_products().values_list('price', flat=True)
        try:
            rslt = max(prices)
        except:
            pass
        return rslt

    def get_products(self):
        """
        Для категорий список товаров формируется из добавленных товаров
        и товаров, подходящих под параметры категории
        """

        return self.products.filter(show=True)

    def full_path(self):
        """
        Get url path ancestors
        """
        path = []
        for ancestor in self.tree.get().get_ancestors(ascending=False):
            if ancestor.content_object.slug:
                path.append(ancestor.content_object.slug)
        if self.slug:
            path.append(self.slug)
        return '/'.join(path)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        object_saved.send(sender=self.__class__, object=self)


class FireResistance(models.Model):
    class Meta:
        verbose_name = u"предел огнестойкости"
        verbose_name_plural = u"пределы огнестойкости"
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(verbose_name=u'наименование', max_length=255)
    image = models.FileField(
        verbose_name=u'изображение',
        upload_to='upload/fireresistance',
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class ItemType(models.Model):
    class Meta:
        verbose_name = u"вид изделия"
        verbose_name_plural = u"виды изделий"
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(verbose_name=u'наименование', max_length=255)
    width = models.CharField(verbose_name=u'ширина', max_length=255, help_text=u'мм', blank=True, null=True)
    height = models.CharField(verbose_name=u'высота', max_length=255, help_text=u'мм', blank=True, null=True)
    fire_resistance = models.ForeignKey(
        FireResistance,
        verbose_name=u'Огнестойкость',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    show_in_filter = models.BooleanField(verbose_name=u'Отображать в фильтре', default=False)

    def __str__(self):
        return self.name


class DocType(models.Model):
    class Meta:
        verbose_name = u"вид документа"
        verbose_name_plural = u"виды документов"
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(verbose_name=u'наименование', max_length=255)
    image = models.FileField(verbose_name=u'изображение', upload_to='upload/doctypes', blank=True, null=True)

    def __str__(self):
        return self.name


class DocImage(ImageModel):
    class Meta:
        verbose_name = u"фото"
        verbose_name_plural = u"фотографии"
        ordering = ('order_key',)

    class IKOptions:
        spec_module = ATTACHMENT_IKSPECS
        cache_dir = ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    order_key = models.PositiveIntegerField(verbose_name=u'Порядок', null=True, blank=True)
    image = ImagePreviewField(verbose_name=u'изображение', upload_to='upload/docs')
    doc = models.ForeignKey('Doc', related_name='images', on_delete=models.CASCADE)


IMG_TYPES = (
    (u'сертификат', u'сертификат'),
    (u'паспорт изделия', u'паспорт изделия'),
    (u'протокол испытаний', u'протокол испытаний'),
    (u'лицензия', u'лицензия'),
    (u'схема конструкции', u'схема конструкции'),
)


class Doc(models.Model):
    class Meta:
        verbose_name = u"документ"
        verbose_name_plural = u"документы"
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)
    name = models.CharField(verbose_name=u'наименование', max_length=255)
    doc_type = models.ForeignKey(
        DocType,
        verbose_name=u'вид документа',
        max_length=255,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    type = models.CharField(verbose_name=u'тип документа', choices=IMG_TYPES, max_length=255, null=True)
    cert_number = models.CharField(verbose_name=u'номер документа', max_length=255, blank=True, null=True)
    cert_series = models.CharField(verbose_name=u'серия документа', max_length=255, blank=True, null=True)
    cert_end_date = models.DateField(verbose_name=u'срок действия документа', blank=True, null=True)
    gost_number = models.CharField(verbose_name=u'ГОСТ', max_length=255, blank=True, null=True)
    tu_number = models.CharField(verbose_name=u'ТУ', max_length=255, blank=True, null=True)
    item_types = models.ManyToManyField(ItemType, verbose_name=u'Виды изделий', related_name='docs')
    description = HTMLField(verbose_name=u'Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class Facing(models.Model):
    class Meta:
        verbose_name = u"тип отделки"
        verbose_name_plural = u"типы отделки"
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(verbose_name='название', max_length=50)
    color = models.CharField(verbose_name='цвет', max_length=255, blank=True, null=True)

    @property
    def images(self):
        return AttachmentImage.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(Facing),
            role=settings.ROLE_GALLERY
        )

    def __str__(self):
        return self.name


class Property(models.Model):
    class Meta:
        verbose_name = u'Параметр'
        verbose_name_plural = u'Параметры'
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(
        verbose_name=u'Название',
        max_length=400
    )
    slug = models.SlugField(
        verbose_name=u'Слаг свойства',
        max_length=200, unique=True, null=True,
        blank=True,
    )
    show_on_filter = models.BooleanField(
        verbose_name=u'Отображать в фильтре',
        default=True,
    )
    show_on_item_desc = models.BooleanField(
        verbose_name=u'отображать в списке кратких характеристик',
        default=False,
    )
    optional = models.BooleanField(
        verbose_name=u'необязательный',
        default=False,
    )

    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)
        parameter_saved.send(sender=self.__class__, object=self)

    def __str__(self, *args, **kwargs):
        return self.name


class Value(models.Model):
    class Meta:
        verbose_name = u'Значение параметра'
        verbose_name_plural = u'Значения параметров'
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    default = models.BooleanField(
        verbose_name=u'Использовать по умолчанию',
        default=False,
    )
    name = models.CharField(
        verbose_name=u'Введите значение',
        max_length=400
    )
    option_name = models.CharField(
        verbose_name=u'Название опции',
        max_length=400,
        null=True,
        blank=True,
    )
    property = models.ForeignKey(
        Property,
        verbose_name=u'Параметр',
        on_delete=models.CASCADE,
        related_name='values',
        null=True
    )
    extra_charge = models.PositiveIntegerField(
        verbose_name='наценка',
        default=0,
    )
    description = models.TextField(verbose_name='Описание', blank=True, null=True, )

    def __str__(self, *args, **kwargs):
        return self.name

    def save(self, *args, **kwargs):
        super(Value, self).save(*args, **kwargs)
        value_saved.send(sender=self.__class__, object=self, property=self.property, default=self.default)


class Parameter(models.Model):
    class Meta:
        verbose_name = u'Параметр'
        verbose_name_plural = u'Параметры'
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    property = models.ForeignKey(
        Property,
        verbose_name=u'Параметр',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    value = models.ForeignKey(
        Value,
        verbose_name=u'Значение',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_parameters',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_parameters',
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='section_parameters',
        blank=True,
        null=True,
    )


class AddParameter(models.Model):
    class Meta:
        verbose_name = u'Доп. Параметр'
        verbose_name_plural = u'Доп. Параметры'
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    property = models.ForeignKey(
        Property,
        verbose_name=u'Параметр',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    values = models.ManyToManyField(
        Value,
        verbose_name=u'Доп. параметры',
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_add_parameters',
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='section_add_parameters',
        blank=True,
        null=True,
    )


class FacingColor(models.Model):
    class Meta:
        verbose_name = 'цвет отделки'
        verbose_name_plural = 'цвета отделки'
        ordering = ('order_key',)

    class IKOptions:
        spec_module = ATTACHMENT_IKSPECS
        cache_dir = ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    order_key = models.PositiveIntegerField(verbose_name="Порядковый номер", default=0, blank=False, null=False)
    name = models.CharField(verbose_name="наименование", max_length=255)
    color = models.CharField(
        verbose_name="цвет",
        help_text='Например: #fff',
        max_length=255,
        blank=True,
        null=True,
    )
    facing = models.ManyToManyField(
        Facing,
        related_name='facing_colors',
        verbose_name=u'Варианты отделки',
        blank=True,
    )
    image = models.FileField(
        verbose_name=u'изображение',
        upload_to=ATTACHMENT_UPLOAD_DIR,
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class FacingPrint(models.Model):
    class Meta:
        verbose_name = 'рисунок отделки'
        verbose_name_plural = 'рисунки отделки'
        ordering = ('order_key',)

    class IKOptions:
        spec_module = ATTACHMENT_IKSPECS
        cache_dir = ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    order_key = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(verbose_name="наименование", max_length=255)
    facing = models.ManyToManyField(
        Facing,
        related_name='facing_prints',
        verbose_name=u'Варианты отделки',
        blank=True,
    )
    image = ImagePreviewField(
        verbose_name=u'изображение',
        upload_to=ATTACHMENT_UPLOAD_DIR,
        blank=True, null=True
    )

    def __str__(self):
        return self.name