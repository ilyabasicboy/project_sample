# Generated by Django 2.2.27 on 2022-03-11 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='show_in_reviews_block',
            field=models.BooleanField(default=False, verbose_name='Отображать в блоке "Отзывы" на сайте'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.date(2022, 3, 11), verbose_name='Дата отправки отзыва'),
        ),
    ]
