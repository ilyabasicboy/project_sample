import datetime
from django.utils.deprecation import MiddlewareMixin

class RequestCookies(MiddlewareMixin):

    def process_response(self, request, response):

        """ Set's http_referer in cookies if it's not equal to own domain """

        max_age = 2592000
        expires = datetime.datetime.now() + datetime.timedelta(seconds=max_age)
        if 'HTTP_REFERER' in request.META and request.META['HTTP_HOST'] not in request.META.get('HTTP_REFERER'):
            if 'HTTP_X_FORWARDED_HOST' in request.META and request.META['HTTP_X_FORWARDED_HOST'] not in request.META.get('HTTP_REFERER'):
                response.set_cookie(
                    'source', request.META.get('HTTP_REFERER'),
                    expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
                    max_age=max_age
                )
        elif 'utm_source' in request.GET:
            response.set_cookie(
                'source', request.GET['utm_source'],
                expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
                max_age=max_age
            )
        return response
