from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.crypto import get_random_string
from account_module.forms import RegisterForm, LoginForm, ForgetPassForm, ResetePassForm
from .models import User
from django.http import Http404, HttpResponse, HttpRequest
from django.contrib.auth import login, logout
from utils.email_service import send_email


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_pass = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'email exist')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=True,
                    username=user_email,
                )
                new_user.set_password(user_pass)
                new_user.save()
                send_email('فعالسازی حساب کاربری',
                           new_user.email,
                           {'user': new_user},
                           'emails/active_account.html')
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری فعال نیست')
                else:
                    is_pass_check = user.check_password(user_pass)
                    if is_pass_check:
                        login(request, user)
                        return redirect(reverse('home-page'))
                    else:
                        login_form.add_error('email', 'کلمه عبور یافت نشد')
            else:
                login_form.add_error('email', 'کاربر یافت نشد!')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                pass
        raise Http404


class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgetPassForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgetPassForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور',
                           user.email,
                           {'user': user},
                           'emails/forgot_pass.html')
                return redirect(reverse('home-page'))
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetePassForm()
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request, active_code):
        reset_pass_form = ResetePassForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            new_user_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(new_user_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))