from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboard.as_view(), name='user_panel_dashboard'),
    path('edit-profile', views.EditUserProfilePage.as_view(), name='edit_profile_page'),
]