# -*- coding:utf-8 -*-
from django.contrib import admin
from catalog.admin import CatalogItemBaseAdmin
from .models import Section, Product, Root, Category
from .forms import ProductAdminForm, SectionAdminForm, RootAdminForm, CategoryAdminForm


class CustomCatalogItemBaseAdmin(CatalogItemBaseAdmin):

    def view_on_site(self, obj):
        return obj.get_absolute_url()


class CategoryInlineAdmin(admin.StackedInline):
    model = Category.products.through
    verbose_name = "Категория"
    verbose_name_plural = "Категории"


@admin.register(Root)
class RootAdmin(CustomCatalogItemBaseAdmin):

    def has_add_permission(self, request):
        return not bool(Root.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    model = Root
    form = RootAdminForm


@admin.register(Product)
class ProductAdmin(CustomCatalogItemBaseAdmin):

    model = Product
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", 'id')
    list_display = ['title', 'google_prefix', 'exclude_google_merchant', 'exclude_direct_yml', 'get_vendor_code']
    list_editable = ['google_prefix', 'exclude_google_merchant', 'exclude_direct_yml']
    inlines = [
        CategoryInlineAdmin,
    ]

    def get_vendor_code(self, obj):
        return obj.id

    get_vendor_code.short_description = u"Артикул"


@admin.register(Section)
class SectionAdmin(CustomCatalogItemBaseAdmin):

    model = Section
    form = SectionAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    list_display = ['title', 'google_prefix', 'google_merchant']
    list_editable = ['google_prefix', 'google_merchant']


@admin.register(Category)
class CategoryAdmin(CustomCatalogItemBaseAdmin):

    model = Category
    form = CategoryAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )


