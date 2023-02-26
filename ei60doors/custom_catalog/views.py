from django.views.generic import TemplateView
from ei60doors.custom_catalog.models import Section, Category, Root, Product
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render


class FilterProductView(TemplateView):
    """ Фильтр каталога """

    template_name = 'catalog/parts/product_list.html'

    def get(self, request):
        ct_id = request.GET.get('ct')
        obj_id = request.GET.get('obj')
        dir = request.GET.get('dir')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if ct_id and obj_id:
            object = ContentType.objects.filter(id=ct_id).first().get_all_objects_for_this_type().filter(id=obj_id).first()
        else:
            object = Root.objects.first()

        products = object.get_products()
        if dir == 'asc':
            products = products.order_by('price')
        elif dir == 'desc':
            products = products.order_by('-price')

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        context ={
            'product_list': products,
        }
        if request.is_ajax():
            html = loader.render_to_string(self.template_name, context, request)
            response_data = {
                'html': html,
                'products_count': products.count(),
            }
            return JsonResponse(response_data)
        return self.render_to_response(context)


def popular_items_pagination(request):

    novelties = Product.objects.filter(show=True,).order_by('-id')

    html = loader.render_to_string(
        'catalog/parts/novelties_list.html',
        {'novelties': novelties},
        request
    )
    response_data = {
        'html': html
    }

    return JsonResponse(response_data)
