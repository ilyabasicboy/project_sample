from django.core.management.base import BaseCommand
from ei60doors.custom_catalog.utils import save_export_yml, save_export_xml, save_direct_yml


class Command(BaseCommand):
    help = ('Update generated yml files')
    can_import_settings = True

    def handle(self, *args, **options):
        save_export_yml()
        save_export_xml()
        save_direct_yml()
