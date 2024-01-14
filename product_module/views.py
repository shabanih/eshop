from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Product
from django.db.models import Avg

# Create your views here.


# def product_list(request):
#     products = Product.objects.all().order_by('price')[:5]
#     return render(request, 'product_list.html', {
#         'products': products,
#     })

class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1




def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {
       'product': product
    })
