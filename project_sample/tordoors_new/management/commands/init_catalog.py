# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tordoors_new.custom_catalog.models import Product, Section, Root
from tordoors_new.management.utils import BLOCK_CONTENT
from catalog.models import TreeItem


UserModel = get_user_model()


class Command(BaseCommand):

    """ Заполнение базы каталога, через fixtures невозможно """

    def handle(self, *args, **options):
        sys.stdout.write("\rCreating catalog...")
        root_page = Root.objects.all().first()
        if not root_page:
            root_page = Root.objects.create(title=u'Каталог', main_content=BLOCK_CONTENT, bottom_content=BLOCK_CONTENT)
            root = TreeItem.objects.create(content_object=root_page)

        root = root_page.tree.get()
        if not root.get_children().exists():
            for i in range(1, 8):
                section = Section.objects.create(title=u'Раздел %d' % i, slug='section-%d' % i, main_content=BLOCK_CONTENT)
                section.tree.get().move_to(root)
            for i in range(1, 17):
                Product.objects.create(title=u'Товар %d' % i, slug='product-%d' % i, main_content=BLOCK_CONTENT)

            section_1 = Section.objects.get(id=1).tree.get()
            for ss in Section.objects.filter(id__in=[2, 3, 4]):
                ss.tree.get().move_to(section_1)

            section_2 = Section.objects.get(id=2).tree.get()
            for p in Product.objects.filter(id__in=[1, 2, 3, 4, 5]):
                p.tree.get().move_to(section_2)

            section_3 = Section.objects.get(id=3).tree.get()
            for p in Product.objects.filter(id__in=[6, 7, 8, 9, 10]):
                p.tree.get().move_to(section_3)

            section_5 = Section.objects.get(id=5).tree.get()
            section_6 = Section.objects.get(id=6).tree.get()
            section_6.move_to(section_5)
            Product.objects.get(id=11).tree.get().move_to(section_6)

            section_7 = Section.objects.get(id=7).tree.get()
            for p in Product.objects.filter(id__in=[12, 13, 14, 15, 16]):
                p.tree.get().move_to(section_7)

            sys.stdout.write(self.style.SUCCESS("        OK\n"))
        else:
            sys.stdout.write(self.style.WARNING("        ALREADY EXIST\n"))

