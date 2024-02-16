from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from product_module.models import Product


def add_product_to_order(request: HttpRequest):
    print(request.GET)
    product_id = request.GET['product_id']
    count = request.GET['count']

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_deleted=False).first()
        if product is not None:
            pass
    else:
        return JsonResponse({
            'status': 'Not logged in'
        })