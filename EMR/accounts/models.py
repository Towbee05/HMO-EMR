from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from djmoney.models.fields import MoneyField
# Create your models here.
# !Model representing how the Coverage table looks in the database. The coverage table consists of all services rendered by the HMO for various plans 
class Coverage(models.Model):
    name = models.CharField(null=False, blank=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Coverage'
# !Model representing how the Plan table looks in the database. The Plan table consists of all plans covered by the HMO available to users based on the amount paid 
class Plans(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES_FIELD = [
        (
            ACTIVE, 'Active'
        ), 
        (
            INACTIVE, 'Inactive'
        )
    ]
    name = models.CharField(max_length=256, null=False, blank=False)
    coverage = models.ManyToManyField(Coverage, related_name='plan')
    price = MoneyField(max_digits=15, decimal_places=2 ,null=False, blank=False, default_currency='NGN')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_FIELD, default=ACTIVE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Plans'
        ordering= ['name']
# !Model representing how the Users table looks in the database. The Users table consists of all users under this HMO, these includes the patients and the hospitals also the HMO admin 
def upload_to(instance, filename):
    return '/'.join(['uploads', str(instance.email), filename])
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    full_name = models.CharField(max_length=140, null=False, blank=False, unique=True, verbose_name=_("Full Name"))
    display_picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()
    def __str__(self):
        return self.email
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh' : str(refresh_token),
            'access' : str(refresh_token.access_token)
        }
