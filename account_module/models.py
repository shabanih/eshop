from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    avatar = models.CharField(max_length=20, verbose_name='تصویر آواتار', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name="کد فعال سازی ایمیل")

    def __str__(self):
        self.get_full_name()