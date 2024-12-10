# Generated by Django 4.2.13 on 2024-09-01 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0006_alter_sitesettings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='instagram_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на Instagram'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='support_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email обратной связи'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='support_phone',
            field=models.CharField(blank=True, null=True, verbose_name='Телефон обратной связи'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='telegram_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на телеграм'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='whatsapp_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на Whatsapp'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='youtube_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на YouTube'),
        ),
    ]