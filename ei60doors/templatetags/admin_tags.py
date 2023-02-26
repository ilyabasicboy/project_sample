# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_admin_sidebar_models(context):

    """ Получить список ссылок для сайдбара в админке """

    user = context['request'].user
    data = []
    if user.is_superuser or user.has_perm('service.change_sitesettings'):
        data.append({'title': u'Настройки домена', 'url': '/admin/service/sitesettings/'})
    if user.is_superuser or user.has_perm('service.change_errorpage'):
        data.append({'title': u'Страницы ошибок', 'url': '/admin/service/errorpage/'})
    if user.is_superuser or user.has_perm('auth.add_user') or user.has_perm('auth.change_user'):
        data.append({'title': u'Пользователи', 'url': '/admin/auth/user/'})
    if user.is_superuser or user.has_perm('auth.add_group') or user.has_perm('auth.change_group'):
        data.append({'title': u'Группы', 'url': '/admin/auth/group/'})
    return data

