from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active', 'id_delete']
    list_filter = ['title', 'category', 'is_active']
    list_editable = ['is_active', 'price']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)

