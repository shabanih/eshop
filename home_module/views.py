from django.shortcuts import render

# Create your views here.


def index_page(request):
    return render(request, 'index_page.html')


def contact_us(request):
    return render(request, 'contact.html')


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')