# Generated by Django 4.2.6 on 2023-10-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_catalogue', '0011_remove_category_ceneo_category_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
