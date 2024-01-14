from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        #     validators.EmailValidator,
        # ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        # ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_pass = self.cleaned_data.get('confirm_password')

        if password == confirm_pass:
            return confirm_pass
        raise ValidationError('کلمه عبور با تکرار آن یکسان نیست!')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        #     validators.EmailValidator,
        # ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        # ]
    )


class ForgetPassForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        #     validators.EmailValidator,
        # ]
    )


class ResetePassForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        # validators=[
        #     validators.MinValueValidator(100),
        # ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )