from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class Plans(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=5 ,null=False, blank=False)

    def __str__(self):
        return self.name
    

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
