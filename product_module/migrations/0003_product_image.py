# Generated by Django 4.2.8 on 2024-01-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0002_productbrand_alter_product_slug_alter_product_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر کالا'),
        ),
    ]
