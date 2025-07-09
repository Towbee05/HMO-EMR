from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from djmoney.models.fields import MoneyField

# Create your models here.
class Coverage(models.Model):
    name = models.CharField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Coverage'

class Plans(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    coverage = models.ManyToManyField(Coverage, related_name='coverage')
    price = MoneyField(max_digits=15, decimal_places=2 ,null=False, blank=False, default_currency='NGN')


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Plans'
        ordering= ['name']


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    full_name = models.CharField(max_length=140, null=False, blank=False, verbose_name=_("Full Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh' : str(refresh_token),
            'access' : str(refresh_token.access_token)
        }
