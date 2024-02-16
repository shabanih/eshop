from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    title_urls = models.CharField(max_length=300, db_index=True, verbose_name="عنوان در url")
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده/نشده')

    def __str__(self):
        return f"{self.title}- {self.title_urls}"


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='نام برند')
    title_urls = models.CharField(max_length=300, db_index=True, verbose_name="نام در url")
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام کالا')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories',
                                      verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to="images/products", null=True, blank=True, verbose_name='تصویر کالا')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, null=True, verbose_name='توضیحات کوتاه', db_index=True)
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, max_length=200, verbose_name='عنوان در Url')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده/نشده')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='آی پی کاربر')
    ip = models.CharField(max_length=30, null=True, blank=True, verbose_name='کاربر')

    def __str__(self):
        return f"{self.product.title} / {self.ip}"


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title
