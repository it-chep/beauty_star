# Generated by Django 4.2.13 on 2024-08-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='TG ID'),
        ),
    ]
