# Generated by Django 4.2.3 on 2023-08-06 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products_catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Subcategory', 'verbose_name_plural': 'Subcategories'},
        ),
    ]
