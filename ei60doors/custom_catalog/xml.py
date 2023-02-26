import os
from ei60doors.custom_catalog.utils import save_export_yml, save_export_xml, save_direct_yml
from django.conf import settings
from django.shortcuts import HttpResponse


def yml_export(request):
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'export_yml.xml')
    if not os.path.exists(path):
        save_export_yml()
    response = HttpResponse(open(path).read(), content_type='text/xml')
    return response


def yml_direct(request):
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'direct_yml.xml')
    if not os.path.exists(path):
        save_direct_yml()
    response = HttpResponse(open(path).read(), content_type='text/xml')
    return response


def xml_export(request):
    dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    path = os.path.join(dir, 'export_xml.xml')
    if not os.path.exists(path):
        save_export_xml()
    response = HttpResponse(open(path).read(), content_type='text/xml')
    return response
