# Generated by Django 4.2.13 on 2024-08-05 23:47

from django.db import migrations, models
import main_site.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0003_sitesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=main_site.models.upload_to_worker_photo)),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='Цена за штуку')),
                ('ordering_number', models.IntegerField(blank=True, null=True, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Товар с витрины',
                'verbose_name_plural': 'Товары с витрины',
            },
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='favicon',
            field=models.ImageField(upload_to=main_site.models.upload_to_worker_photo),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='logo',
            field=models.ImageField(upload_to=main_site.models.upload_to_worker_photo),
        ),
    ]
