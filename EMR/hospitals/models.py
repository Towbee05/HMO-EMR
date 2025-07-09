from django.db import models
from accounts.models import Plans
from django.core.validators import RegexValidator
import re
from django.contrib.auth.hashers import make_password, check_password
import uuid
from datetime import date
from accounts.models import User
from django.utils import timezone

# Create your models here.

regex = r'^((([+](234){1}+(70|80|90|81))|(070|080|090|081))[0-9]{8})$'

class Hospitals(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    HOSPITAL_STATUS_CHOICES = [
        (
            ACTIVE, 'Active',
        ),
        (
            INACTIVE, 'Inactive'
        )
    ]
    id= models.UUIDField(blank=False, null=False, primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank= False, null= False)
    email = models.EmailField(blank=False, null=False, max_length=120, unique=True)
    location = models.CharField(blank=False, null= False)
    status = models.CharField(max_length=20, choices=HOSPITAL_STATUS_CHOICES, default=ACTIVE)
    phone = models.CharField(null=False, blank=False, unique=True,validators=[RegexValidator(regex, message="Invalid Phone number entered!!", code='invalid_phone_no')])
    services = models.TextField(verbose_name='services')
    plans = models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True, related_name='hospitals')
    accredition_license = models.CharField(blank=False, null=False, default='null')
    accredition_status = models.CharField(blank=False, null=False, default='active')
    accredition_expires = models.DateField(default=date.today)  
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    display_picture = models.ImageField(upload_to='uploads/', null=True, blank=True)
    # password = models.CharField(null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hospital', null=True)

    class Meta:
        verbose_name_plural = "Hospitals"
        ordering = ['-date_joined']

    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    