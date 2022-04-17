# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView
from tordoors_new.custom_catalog.models import Section, Product, Category, Property, Root


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
            if request.GET['fireproof'] == '0':
                product_ids = [
                    prod.id for prod in products if
                    prod.get_item_type().fire_resistance is None
                ]
            else:
                product_ids = [
                    prod.id for prod in products if
                    prod.get_item_type().fire_resistance and
                    prod.get_item_type().fire_resistance.id == int(request.GET['fireproof'])
                ]

            products = products.filter(id__in=product_ids)

        if 'facing' in request.GET and request.GET['facing']:
            products = products.filter(facing=request.GET['facing'])

        if 'dir' in request.GET:
            if request.GET['dir'] == 'asc':
                products = products.order_by('price')
            elif request.GET['dir'] == 'desc':
                products = products.order_by('-price')

        """Подбор по динамическим параметрам"""
        parameters_all = Property.objects.filter(show_on_filter=True)
        # Взять список значений парметров из request.GET
        try:
            parameters = [
                int(request.GET[param.slug]) for param in parameters_all if
                param.slug in request.GET and request.GET[param.slug]
            ]
        except:
            parameters = []

        """
        Проводится цикл по товарам. Если список с id значений параметров, выбранных в фильтре
        есть в списке значений параметров товара, товар добавляется в список
        """
        if parameters:
            products = [
                product for product in products if
                all(val in list(product.get_parameters().values_list('value', flat=True)) for val in parameters)
            ]

        """ Товары для счетчика необходимо считать до добавления статей в них """
        products_count = len(products)

        try:
            articles = object.articles.all()
            if articles and len(products) >= 8:
                for i in range(len(products) / 8):
                    products.insert(9 * (i + 1) - 1, articles[i])
        except:
            pass

        context = {
            'object_list': products,
            'products_count': products_count
        }

        return self.render_to_response(context)
