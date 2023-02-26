from pages.models import Page
from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponseNotFound


def pages_list_pagination(request, obj_id):

    page = Page.objects.filter(id=obj_id).first()
    if page:
        children = page.get_children_for_frontend()

        html = loader.render_to_string(
            'pages/parts/card_list.html',
            {'children': children, 'current_page': page},
            request
        )
        response_data = {
            'html': html
        }

        return JsonResponse(response_data)
    return HttpResponseNotFound
