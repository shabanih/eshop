# Generated by Django 5.0.1 on 2024-02-09 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='title_urls',
            field=models.CharField(db_index=True, default='brand', max_length=300, verbose_name='نام در url'),
            preserve_default=False,
        ),
    ]
