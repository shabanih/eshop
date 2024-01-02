from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.


def contact_us_page(request):
    if request.method == 'POST':
        print(request.POST['email'])
        print(request.POST['fullName'])
        print(request.POST['subject'])
        print(request.POST['message'])
        return redirect(reverse('home-page'))
    return render(request, 'contact_module/contact_us_page.html')