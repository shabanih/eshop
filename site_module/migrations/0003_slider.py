# Generated by Django 4.2.8 on 2024-01-14 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0002_footerlinkbox_alter_sitesetting_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('url', models.CharField(max_length=200, verbose_name='لینک')),
                ('url_title', models.CharField(max_length=200, verbose_name='عنوان لینک')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('image', models.ImageField(upload_to='images/slider/', verbose_name='تصویر اسلایدر')),
            ],
        ),
    ]