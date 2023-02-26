# Generated by Django 2.2.28 on 2022-12-06 09:49

from django.db import migrations, models
import django.db.models.deletion
import ei60doors.custom_catalog.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0010_auto_20211220_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Root',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True, verbose_name='Show on site')),
                ('title', models.CharField(max_length=400, verbose_name='название')),
                ('long_title', models.CharField(blank=True, max_length=400, null=True, verbose_name='длинное название')),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'корневая страница',
                'verbose_name_plural': 'корневая страница',
            },
            bases=(models.Model, ei60doors.custom_catalog.models.CatalogMixin),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True, verbose_name='Show on site')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Datetime last modified')),
                ('slug', models.SlugField(help_text='The slug will be used to create the page URL, it must be unique among the other pages of the same level.', max_length=255, unique=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=400, verbose_name='название')),
                ('long_title', models.CharField(blank=True, max_length=400, null=True, verbose_name='длинное название')),
                ('habarytes', models.TextField(blank=True, max_length=255, null=True, verbose_name='Габариты')),
                ('construction', models.IntegerField(blank=True, choices=[(0, 'Однопольная'), (1, 'Полуторапольная'), (2, 'Двупольная')], null=True, verbose_name='Конструкция')),
                ('fireproof', models.IntegerField(blank=True, choices=[(0, 'Ei-30'), (1, 'Ei-60'), (2, 'Ei-90')], null=True, verbose_name='Огнестойкость')),
                ('readiness', models.CharField(blank=True, max_length=255, null=True, verbose_name='Готовность')),
                ('delivery', models.CharField(blank=True, max_length=255, null=True, verbose_name='Доставка')),
                ('mounting', models.CharField(blank=True, max_length=500, null=True, verbose_name='монтаж')),
                ('specs', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Характеристики')),
                ('services', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Услуги')),
                ('finish', models.ManyToManyField(blank=True, limit_choices_to={'status': 1, 'template': 'pages/finish.html'}, related_name='finish_sections', to='pages.Page', verbose_name='Варианты отделки')),
                ('gallery', models.ForeignKey(blank=True, limit_choices_to={'status': 1, 'template': 'pages/gallery.html'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gallery_sections', to='pages.Page', verbose_name='Галерея')),
            ],
            options={
                'verbose_name': 'раздел',
                'verbose_name_plural': 'разделы',
            },
            bases=(models.Model, ei60doors.custom_catalog.models.CatalogMixin),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True, verbose_name='Show on site')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Datetime last modified')),
                ('slug', models.SlugField(help_text='The slug will be used to create the page URL, it must be unique among the other pages of the same level.', max_length=255, unique=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=400, verbose_name='название')),
                ('long_title', models.CharField(blank=True, max_length=400, null=True, verbose_name='длинное название')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='цена')),
                ('old_price', models.PositiveIntegerField(default=0, verbose_name='старая цена')),
                ('habarytes', models.TextField(blank=True, max_length=255, null=True, verbose_name='Габариты')),
                ('construction', models.IntegerField(blank=True, choices=[(0, 'Однопольная'), (1, 'Полуторапольная'), (2, 'Двупольная')], null=True, verbose_name='Конструкция')),
                ('fireproof', models.IntegerField(blank=True, choices=[(0, 'Ei-30'), (1, 'Ei-60'), (2, 'Ei-90')], null=True, verbose_name='Огнестойкость')),
                ('readiness', models.CharField(blank=True, max_length=255, null=True, verbose_name='Готовность')),
                ('delivery', models.CharField(blank=True, max_length=255, null=True, verbose_name='Доставка')),
                ('mounting', models.CharField(blank=True, max_length=500, null=True, verbose_name='монтаж')),
                ('specs', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Характеристики')),
                ('services', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Услуги')),
                ('finish', models.ManyToManyField(blank=True, limit_choices_to={'status': 1, 'template': 'pages/finish.html'}, related_name='finish_products', to='pages.Page', verbose_name='Варианты отделки')),
                ('gallery', models.ForeignKey(blank=True, limit_choices_to={'status': 1, 'template': 'pages/gallery.html'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gallery_products', to='pages.Page', verbose_name='Галерея')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True, verbose_name='Show on site')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Datetime last modified')),
                ('slug', models.SlugField(help_text='The slug will be used to create the page URL, it must be unique among the other pages of the same level.', max_length=255, unique=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=400, verbose_name='название')),
                ('long_title', models.CharField(max_length=400, verbose_name='длинное название')),
                ('products', models.ManyToManyField(blank=True, to='custom_catalog.Product', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
            bases=(models.Model, ei60doors.custom_catalog.models.CatalogMixin),
        ),
    ]
