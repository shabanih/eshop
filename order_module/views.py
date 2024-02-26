import json
import time

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from order_module.models import Order, OrderDetail
from product_module.models import Product

# #? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# MERCHANT = "edb784f9-a0d6-4fe3-b2f0-b05b70eabfe9"


MERCHANT = "3d6d6a26-c139-49ac-9d8d-b03a8cdf0fdd"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    print(request.GET)
    product_id = int(request.GET.get("product_id"))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            "status": "Not Valid!",
            'text': "مقدار وارد شده صحیح نمیباشد",
            'confirm_button_text': "باشه ممنون",
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()

            else:
                new_order = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_order.save()

            return JsonResponse({
                'status': 'success',
                'text': "کالا با موفقیت به سبد خرید شما اضافه شد",
                'confirm_button_text': "ممنون",
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'Not Found',
                'text': "کالای مورد نظر یافت نشد",
                'confirm_button_text': "باشه ممنون",
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': "برای اضافه کردن کالا به سید خرید مبایست ابتدا وارد سایت شوید",
            'confirm_button_text': "ورود به سایت",
            'icon': 'error'
        })


@login_required
def request_payment(request: HttpRequest):

    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,

        # "metadata": {"mobile": mobile, "email": email}
    }
    print(req_data)
    data = json.dumps(req_data)
    req_header = {'content-type': 'application/json', 'content-length': str(len(req_data))}
    print("Request Header:", req_header)

    print("Request URL:", ZP_API_REQUEST)
    print("Request Data:", data)
    print("Request Headers:", req_header)

    response = requests.post(url=ZP_API_REQUEST, data=data, headers=req_header)

    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)

        if response_json['Status'] == 100:
            return {'status': True, 'url': ZP_API_STARTPAY + str(response_json['Authority']),
                    'authority': response_json['Authority']}
        else:
            return {'status': False, 'code': str(response_json['Status'])}
    else:
        print("Error Response Content:", response.content)
        return {'status': False, 'error': f'Request failed with status code {response.status_code}'}

    # authority = req.json()['data']['authority']
    # if len(req.json()['errors']) == 0:
    #     return redirect(ZP_API_STARTPAY.format(authority=authority))
    # else:
    #     e_code = req.json()['errors']['code']
    #     e_message = req.json()['errors']['message']
    #     return HttpResponse("Error code")


# @login_required
# def verify_payment(request: HttpRequest):
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     total_price = current_order.calculate_total_price()
#     t_authority = request.GET['Authority']
#     if request.GET.get('Status') == 'OK':
#         req_header = {"accept": "application/json", "content-type": "application/json'"}
#         req_data = {
#             "merchant_id": MERCHANT,
#             "amount": total_price * 10,
#             "authority": t_authority
#         }
#         req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
#         if len(req.json()['errors']) == 0:
#             t_status = req.json()['data']['code']
#             if t_status == 100:
#                 current_order.is_paid = True
#                 current_order.payment_date = time.time()
#                 current_order.save()
#                 ref_str = req.json()['data']['ref_id']
#                 return render(request, 'order_module/payment_result.html', {
#                     'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
#                 })
#             elif t_status == 101:
#                 return render(request, 'order_module/payment_result.html', {
#                     'info': 'این تراکنش قبلا ثبت شده است'
#                 })
#             else:
#                 # return HttpResponse('Transaction failed.\nStatus: ' + str(
#                 #     req.json()['data']['message']
#                 # ))
#                 return render(request, 'order_module/payment_result.html', {
#                     'error': str(req.json()['data']['message'])
#                 })
#         else:
#             e_code = req.json()['errors']['code']
#             e_message = req.json()['errors']['message']
#             # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#             return render(request, 'order_module/payment_result.html', {
#                 'error': e_message
#             })
#     else:
#         return render(request, 'order_module/payment_result.html', {
#             'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
#         })


# def request_payment(request: HttpRequest):
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     total_price = current_order.calculate_total_price()
#     if total_price == 0:
#         return redirect(reverse('user_basket_page'))
#
#     req_data = {
#         "merchant_id": MERCHANT,
#         "amount": total_price * 10,
#         "callback_url": CallbackURL,
#         "description": description,
#         # "metadata": {"mobile": mobile, "email": email}
#     }
#     req_header = {"accept": "application/json", "content-type": "application/json'"}
#     req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
#     authority = req.json()['data']['authority']
#     if len(req.json()['errors']) == 0:
#         return redirect(ZP_API_STARTPAY.format(authority=authority))
#     else:
#         e_code = req.json()['errors']['code']
#         e_message = req.json()['errors']['message']
#         return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify_payment(request):
    # print(request.user)
    # print(request.user.id)
    authority = request.GET['authority']
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
