from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from user_panel_module.forms import EditProfileModelForm


# Create your views here.
class UserPanelDashboard(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


class EditUserProfilePage(View):
    def get(self, request):
        edit_form = EditProfileModelForm()
        context = {
            'form': edit_form
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request, *args, **kwargs):
        return render(request, 'user_panel_module/edit_profile_page.html', {})


def user_menu_component(request):
    return render(request, 'user_panel_module/components/user_menu_component.html')