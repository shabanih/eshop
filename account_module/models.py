from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/Profile', verbose_name='تصویر آواتار', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name="کد فعال سازی ایمیل")
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')

    def __str__(self):
       if self.first_name is not  '' and self.last_name is not  '':
           return self.get_full_name()
       return self.email