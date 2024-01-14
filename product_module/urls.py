from django.conf.urls.static import static
from django.urls import path

from eshop import settings
from . import views

urlpatterns = [
   path('', views.ProductListView.as_view()),
   path('<slug:slug>', views.product_detail, name='product-detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)