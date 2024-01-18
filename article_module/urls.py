from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='article_list'),
    path('<pk>', views.ArticleDetailView.as_view(), name='article_detail')
]