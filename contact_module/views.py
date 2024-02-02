from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from contact_module.forms import ContactUsModelForm
from site_module.models import SiteSetting


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact-us/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting

        return context