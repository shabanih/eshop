# Generated by Django 5.0.1 on 2024-02-15 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_rename_id_delete_productcategory_is_delete_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
            ],
        ),
    ]
