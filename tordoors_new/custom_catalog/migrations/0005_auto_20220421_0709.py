# Generated by Django 2.2.27 on 2022-04-21 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20211220_1131'),
        ('custom_catalog', '0004_auto_20220411_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='door_samples',
            field=models.ForeignKey(blank=True, limit_choices_to={'template': 'pages/gallery.html'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.Page', verbose_name='примеры дверей'),
        ),
        migrations.AddField(
            model_name='product',
            name='show_interior_sample',
            field=models.BooleanField(default=False, verbose_name='Отображать блок "пример в интерьере"'),
        ),
        migrations.AddField(
            model_name='section',
            name='show_interior_sample',
            field=models.BooleanField(default=True, help_text='Наследуется дочерним товарам', verbose_name='Отображать блок "пример в интерьере"'),
        ),
    ]
