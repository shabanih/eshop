from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس ')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن ')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس ')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل ')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی سایت')

    def __str__(self):
        return self.site_name


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/slider/', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزئیات محصولات'
        about_us = 'about_us', 'درباره ما',

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='images/site-banner/', verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

