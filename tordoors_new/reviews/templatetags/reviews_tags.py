from django import template
from ..models import Review


register = template.Library()

@register.simple_tag()
def get_reviews_list():

    """ Возвращает корневую новостей """

    return Review.objects.filter(show=True).order_by('-date')