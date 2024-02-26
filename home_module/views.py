from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list

import sys
sys.stdout.reconfigure(encoding='utf-8')


class HomeView(TemplateView):
    template_name = 'index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(visited_count=Count('productvisit')).order_by('-visited_count')[:12]
        context['latest_products'] = group_list(latest_products)
        context['most_visited_products'] = group_list(most_visited_products)
        categories = ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True, is_delete=False, product_count__gt=0)[:6]
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)

        context['categories_products'] = categories_products

        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]
        context['most_bought_products'] = group_list(most_bought_products)

        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_box = FooterLinkBox.objects.all()
    for item in footer_link_box:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_box': footer_link_box
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'about_us.html'
    
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context