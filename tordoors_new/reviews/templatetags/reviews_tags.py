from django import template
from ..models import Review


register = template.Library()

@register.simple_tag()
def get_reviews_list():

    """ Возвращает корневую новостей """

    return Review.objects.filter(show_in_reviews_block=True).order_by('?')