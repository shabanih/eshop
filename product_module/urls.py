from django.conf.urls.static import static
from django.urls import path

from eshop import settings
from . import views

urlpatterns = [
   path('', views.ProductListView.as_view(), name='product-list'),
   path('cat/<cat>', views.ProductListView.as_view(), name='product-categories-list'),
   path('brand/<brand>', views.ProductListView.as_view(), name='product-by_brands'),
   path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)