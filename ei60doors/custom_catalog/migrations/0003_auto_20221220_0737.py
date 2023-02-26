# Generated by Django 2.2.28 on 2022-12-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_catalog', '0002_auto_20221206_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='exclude_google_merchant',
            field=models.BooleanField(default=False, verbose_name='Не выгружать в Google Merchant'),
        ),
        migrations.AddField(
            model_name='product',
            name='google_prefix',
            field=models.CharField(blank=True, help_text='Добавляет префикс к длинному названию товара в google merchant', max_length=400, null=True, verbose_name='Префикс Google Merchant'),
        ),
        migrations.AddField(
            model_name='section',
            name='google_merchant',
            field=models.BooleanField(default=True, help_text='Наследуется в товары', verbose_name='Выгружать в Google Merchant'),
        ),
        migrations.AddField(
            model_name='section',
            name='google_prefix',
            field=models.CharField(blank=True, help_text='Добавляет префикс к длинному названию дочерних товаров в google merchant', max_length=400, null=True, verbose_name='Префикс Google Merchant'),
        ),
    ]