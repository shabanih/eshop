from django.contrib import admin
from . import models


# Register your models here.

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']
    list_editable = ['url_title', 'parent', 'is_active']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_editable = ['is_active']


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'parent']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)