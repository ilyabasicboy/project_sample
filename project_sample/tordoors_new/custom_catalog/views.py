# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView
from catalog.utils import get_sorted_content_objects, get_content_objects
from tordoors_new.custom_catalog.models import Section, Product, Category, Property, Root
from tordoors_new.custom_catalog.models import get_sections_with_parameters, get_category_products


class FilterProductView(TemplateView):
    """ Фильтр каталога """
    template_name = 'catalog/parts/block_cards.html'

    def get(self, request):
        if 'object' in request.GET and 'c_type' in request.GET:
            obj_id = request.GET['object']
            model = request.GET['c_type']

            if model == 'section':
                object = Section.objects.get(id=obj_id)
                products = object.get_products()
            elif model == 'category':
                object = Category.objects.get(id=obj_id)
                products = object.get_products()
            else:
                object = Root.objects.all().first()
                products = object.get_products()
        else:
            self.template_name = 'catalog/parts/block_cards.html'
            products = Product.objects.filter(show=True)
            product_ids = [prod.id for prod in products if prod.get_item_type() and prod.get_item_type().show_in_filter]
            products = products.filter(id__in=product_ids)

        """
        Перенаправление на страницу быстрый подбор двери,
        если запрос из формы "подобрать дверь по параметрам"
        """
        if not request.is_ajax():
            self.template_name = 'catalog/fast_filter_page.html'

        if 'min_price' in request.GET and request.GET['min_price']:
            products = products.filter(
                price__gte=request.GET['min_price']
            )
        if 'max_price' in request.GET and request.GET['max_price']:
            products = products.filter(
                price__lte=request.GET['max_price']
            )
        """
        Огнестойкость вида изделия может отсутствовать у товара,
        но наследоваться от разделов
        """
        if 'fireproof' in request.GET and request.GET['fireproof']:
            product_ids = []
            for prod in products:
                try:
                    if prod.get_item_type().fire_resistance.id == int(request.GET['fireproof']):
                        product_ids.append(prod.id)
                except:
                    pass
            products = products.filter(id__in=product_ids)

        if 'facing' in request.GET and request.GET['facing']:
            products = products.filter(facing=request.GET['facing'])

        if 'dir' in request.GET:
            if request.GET['dir'] == 'asc':
                products = products.order_by('price')
            elif request.GET['dir'] == 'desc':
                products = products.order_by('-price')

        """Подбор по динамическим параметрам"""
        parameters = Property.objects.filter(show_on_filter=True)
        for parameter in parameters:
            if parameter.slug in request.GET and request.GET[parameter.slug]:
                value = request.GET[parameter.slug]
                """ 
                В результат добавляются товары с заполненными указанными параметрами,
                а так же с пустыми указанными параметрами,
                если у разделов-предков заполнен данный параметр.
                """
                sections = get_sections_with_parameters(parameter, value)
                products = products.filter(
                    product_parameters__property=parameter,
                    product_parameters__value=value
                ) | products.filter(
                    tree__parent__id__in=sections,
                    product_parameters__property=parameter,
                    product_parameters__value=None
                )

        """ Товары для счетчика необходимо считать до добавления статей в них """
        products_count = len(products)

        try:
            articles = object.articles.all()
            if articles and len(products) >= 8:
                products = list(products)
                for i in range(len(products) / 8):
                    products.insert(9 * (i + 1) - 1, articles[i])
        except:
            pass

        context = {
            'object_list': products,
            'products_count': products_count
        }

        return self.render_to_response(context)
