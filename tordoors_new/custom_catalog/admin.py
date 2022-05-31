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


class CustomCatalogItemBaseAdmin(CatalogItemBaseAdmin):

    def view_on_site(self, obj):
        return obj.get_absolute_url()


@admin.register(Root)
class RootAdmin(CustomCatalogItemBaseAdmin):

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
    classes = ['collapse']

    # Убрать возможность добавлять инлайн параметра вручную
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AddParameterInline(admin.TabularInline):
    exclude = ['order_key']
    model = AddParameter
    form = AddParameterAdminForm
    ordering = ['property__order_key']
    classes = ['collapse']

    # Убрать возможность добавлять инлайн доп. параметра вручную
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductImageInlines(SortableInlineAdminMixin, admin.TabularInline):
    class Meta:
        ordering = ('order_key',)

    model = ProductImage
    form = ProductImageForm
    extra = settings.ATTACHMENT_EXTRA_IMAGES
    fields = ['order_key', 'image', 'side', 'color', 'print']

    classes = ['collapse']


class SectionImageInlines(admin.TabularInline):
    class Meta:
        ordering = ('order_key',)

    model = ProductImage
    form = ProductImageForm
    extra = settings.ATTACHMENT_EXTRA_IMAGES
    fields = ['order_key', 'image', 'facing', 'side', 'color', 'print']


@admin.register(Product)
class ProductAdmin(CustomCatalogItemBaseAdmin):

    model = Product
    form = ProductAdminForm
    inlines = [
        ProductImageInlines,
        ParameterInline,
        AddParameterInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", 'long_title')
    list_display = ['title', 'get_vendor_code', 'item_type', 'price', 'show',]
    list_editable = ['item_type',]

    def get_vendor_code(self, obj):
        return obj.get_vendor_code()

    get_vendor_code.short_description = 'Артикул'


@admin.register(Section)
class SectionAdmin(CustomCatalogItemBaseAdmin):

    model = Section
    form = SectionAdminForm
    inlines = [
        SectionImageInlines,
        ParameterInline,
        AddParameterInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", 'long_title',)


@admin.register(Category)
class CategoryAdmin(CustomCatalogItemBaseAdmin):

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
    list_display = ('name', 'optional', 'show_on_item_desc', 'show_on_yml')
    list_editable = ('optional', 'show_on_item_desc', 'show_on_yml')

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
