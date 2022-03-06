# -*- coding:utf-8 -*-
from django.contrib import admin
from catalog.admin import CatalogItemBaseAdmin
from django.conf import settings
from tordoors_new.custom_catalog.models import Root, Parameter, AddParameter, ProductImage, Product, Section, Category, \
    ItemType, DocImage, Doc, FireResistance, DocType, Property, Value, FacingPrint, FacingColor, Facing
from tordoors_new.custom_catalog.forms import RootAdminForm, ParameterAdminForm, AddParameterAdminForm, \
    ProductImageForm, ProductAdminForm, SectionAdminForm, CategoryAdminForm, DocAdminForm, FacingPrintAdminForm, \
    FacingColorAdminForm
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(Root)
class RootAdmin(CatalogItemBaseAdmin):

    def has_add_permission(self, request):
        return not bool(Root.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    model = Root
    form = RootAdminForm
    fields = ['title', 'long_title', 'top_content', 'bottom_content']


class ParameterInline(admin.TabularInline):
    exclude = ['order_key']
    model = Parameter
    form = ParameterAdminForm
    ordering = ['property__order_key']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AddParameterInline(admin.TabularInline):
    exclude = ['order_key']
    model = AddParameter
    form = AddParameterAdminForm
    ordering = ['property__order_key']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductImageInlines(admin.TabularInline):
    class Meta:
        ordering = ('order_key',)

    model = ProductImage
    form = ProductImageForm
    extra = settings.ATTACHMENT_EXTRA_IMAGES
    fields = ['order_key', 'image', 'side', 'color', 'print']


class SectionImageInlines(admin.TabularInline):
    class Meta:
        ordering = ('order_key',)

    model = ProductImage
    form = ProductImageForm
    extra = settings.ATTACHMENT_EXTRA_IMAGES
    fields = ['order_key', 'image', 'facing', 'side', 'color', 'print']


@admin.register(Product)
class ProductAdmin(CatalogItemBaseAdmin):

    model = Product
    form = ProductAdminForm
    inlines = [
        ProductImageInlines,
        ParameterInline,
        AddParameterInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    list_display = ['title', 'item_type']
    list_editable = ['item_type']


@admin.register(Section)
class SectionAdmin(CatalogItemBaseAdmin):

    model = Section
    form = SectionAdminForm
    inlines = [
        SectionImageInlines,
        ParameterInline,
        AddParameterInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )


@admin.register(Category)
class CategoryAdmin(CatalogItemBaseAdmin):

    model = Category
    form = CategoryAdminForm
    inlines = [
        ParameterInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )


class ItemTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = ItemType
    list_display = ('name', 'width', 'height', 'fire_resistance', 'show_in_filter')
    list_editable = ('width', 'height', 'fire_resistance', 'show_in_filter')
    search_fields = ('name',)
    list_filter = ('fire_resistance', )


class DocImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DocImage
    extra = 0


class DocAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Doc
    inlines = [DocImageInline]
    list_display = ('name', 'doc_type', 'cert_end_date',)
    form = DocAdminForm


class FireResistanceAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = FireResistance
    extra = 0


class DocTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = DocType
    extra = 0

admin.site.register(FireResistance, FireResistanceAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(DocType, DocTypeAdmin)
admin.site.register(Doc, DocAdmin)


class PropertyAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Property
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'optional',)
    list_editable = ('optional',)

admin.site.register(Property, PropertyAdmin)


class ValueAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Value
    list_filter = ('property',)
    search_fields = ('property',)
    list_display = ('name','default',)
    list_editable = ('default',)


admin.site.register(Value, ValueAdmin)


@admin.register(FacingPrint)
class FacingPrintAdmin(admin.ModelAdmin):
    model = FacingPrint
    form = FacingPrintAdminForm


@admin.register(FacingColor)
class FacingColorAdmin(admin.ModelAdmin):
    model = FacingColor
    form = FacingColorAdminForm


admin.site.register(Facing)
