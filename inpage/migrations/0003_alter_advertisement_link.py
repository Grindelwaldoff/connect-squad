# Generated by Django 4.1 on 2023-07-31 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inpage', '0002_alter_advertisement_options_advertisement_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='link',
            field=models.CharField(help_text='вставьте ссылку для рекламной компании', max_length=10000, verbose_name='Реферальная ссылка:'),
        ),
    ]