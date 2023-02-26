from django.db import models
from attachment.settings import ATTACHMENT_UPLOAD_DIR
from ei60doors.custom_catalog.models import Section, Category
from pages.models import Page
from django.core.exceptions import ValidationError


class Advantage(models.Model):

    class Meta:
        verbose_name = u'Преимущество'
        verbose_name_plural = u'Преимущества'
        ordering = ['order_key', ]

    order_key = models.PositiveIntegerField(
        verbose_name=u'',
        default=0,
        blank=False, null=False
    )
    title = models.TextField(
        verbose_name=u'Текст'
    )

    icon = models.FileField(
        verbose_name=u'Иконка',
        null=True,
        blank=True,
        upload_to=ATTACHMENT_UPLOAD_DIR
    )

    def __str__(self):
        return self.title


class CatalogItem(models.Model):
    class Meta:
        verbose_name = u'Блок "каталог"'
        verbose_name_plural = verbose_name
        ordering = ['order_key']

    order_key = models.PositiveIntegerField(verbose_name=u'', default=0, blank=False, null=False)
    section = models.ForeignKey(
        Section,
        verbose_name=u'раздел',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name=u'категория',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def clean(self):
        """Ensure that only one of `section` and `category` can be set."""
        if self.section and self.category or not self.section and not self.category:
            raise ValidationError("Нужно выбрать либо категорию, либо раздел")
        return super(CatalogItem, self).clean()

    def __str__(self):
        return 'Выберите раздел или категорию'

    def get_item(self):
        if self.section:
            return self.section
        else:
            return self.category
