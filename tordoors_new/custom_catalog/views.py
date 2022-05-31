# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.generic import TemplateView
from tordoors_new.custom_catalog.models import Section, Product, Category, Root, Property, Value
from django.template import loader
from django.db.models import Q


class FilterProductView(TemplateView):
    """ Фильтр каталога """
    template_name = 'catalog/parts/block_cards.html'

    def fast_filter_sort(self, products):
        # Какие товары можно отображать.
        # Вид изделия может наследоваться от разделов
        sections = Section.objects.filter(item_type__show_in_filter=True)
        subsections = Section.objects.filter(item_type=None, tree__parent__object_id__in=sections)
        products = products.filter(
            Q(item_type__show_in_filter=True)|
            Q(tree__parent__object_id__in=sections)|
            Q(tree__parent__object_id__in=subsections)
        )

        # Фильтр по огнестойкости
        # Огнестойкость может наследоватсья от разделов
        fireproof = self.request.GET.get('fireproof')
        if fireproof:
            if fireproof == '0':
                sections = sections.filter(item_type__fire_resistance=None)
                subsections = subsections.filter(
                    tree__parent__object_id__in=sections,
                    item_type__fire_resistance=None
                )
                products = products.filter(
                    Q(item_type__fire_resistance=None),
                    Q(tree__parent__object_id__in=sections) |
                    Q(tree__parent__object_id__in=subsections)
                )
            else:
                sections = sections.filter(item_type__fire_resistance=int(fireproof))
                subsections = subsections.filter(
                    tree__parent__object_id__in=sections,
                    item_type__fire_resistance=None
                )
                products = products.filter(
                    Q(item_type__fire_resistance=int(fireproof)) |
                    Q(tree__parent__object_id__in=sections) |
                    Q(tree__parent__object_id__in=subsections)
                )

        facing = self.request.GET.get('facing')
        if facing:
            products = products.filter(facing=facing)

        """Подбор по динамическим параметрам"""
        parameters_all = Property.objects.filter(show_on_filter=True)

        # Список id значений параметров
        parameters = [
            int(self.request.GET.get(param.slug)) for param in parameters_all if
            self.request.GET.get(param.slug)
        ]

        values = Value.objects.filter(id__in=parameters)

        # Поиск товаров по m2m "parameters" товара
        if values.exists():
            for v in values:
                products = v.product_set.filter(id__in=products)

        return products

    def get(self, request):
        self.context = {}
        # Проверка страницы запроса(модель каталога/страница быстрого фильтра)
        obj_id = request.GET.get('object')
        model = request.GET.get('c_type')
        if model and obj_id:
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
            self.context['fast_filter'] = True
            products = Product.objects.filter(show=True)

            # Если есть артикул, пропускаем фильтрацию по параметрам
            vendor_code = self.request.GET.get('vendor_code')
            if vendor_code:
                products = products.filter(id=vendor_code)
            else:
                products = self.fast_filter_sort(products)


        # Подгрузить всю страницу быстрого фильтра, если запрос не асинхронный
        if not request.is_ajax():
            self.template_name = 'catalog/fast_filter_page.html'

        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(
                price__gte=min_price
            )

        max_price = request.GET.get('max_price')
        if max_price:
            products = products.filter(
                price__lte=max_price
            )

        dir = request.GET.get('dir')
        if dir == 'asc':
            products = products.order_by('price')
        elif dir == 'desc':
            products = products.order_by('-price')

        # Посчитать товары перед добавлением статей
        products_count = products.count()

        try:
            articles = object.articles.all()
            if articles and len(products) >= 8:
                for i in range(len(products) / 8):
                    products.insert(9 * (i + 1) - 1, articles[i])
        except:
            pass

        self.context['object_list'] = products
        self.context['products_count'] = products_count

        # При асинхронной подгрузке вернуть словарь с количеством товаров и html(для фронтенда)
        if request.is_ajax():
            html = loader.render_to_string(self.template_name, self.context, request)
            response_data = {
                'html': html,
                'products_count': products_count,
            }
            return JsonResponse(response_data)
        else:
            return self.render_to_response(self.context)
