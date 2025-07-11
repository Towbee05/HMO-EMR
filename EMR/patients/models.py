from django.db import models
from accounts.models import User, Plans
import uuid
from django.core.validators import RegexValidator

# Create your models here.

regex = r'^((([+](234){1}+(70|80|90|81))|(070|080|090|081))[0-9]{8})$'
# !Model representing how the patients table looks in the database. This table handles all patients registered under the HMO
class Patients(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
    GENDER_CHOICES = [
        (   
            MALE, 'Male'
        ),
        (
            FEMALE, 'Female'
        )
    ]

    STATUS_CHOICES = [
        (
            ACTIVE, 'Active'
        ),
        (
            INACTIVE, 'Inactive'
        )
    ]

    id = models.UUIDField(blank=False, null=False, primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length= 250, blank=False, null= False)
    age = models.IntegerField(blank=False, null=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=7)
    email = models.EmailField(max_length=120, blank=False, null= False, unique=True)
    phone = models.CharField(null=False, blank=False, unique=True, validators=[RegexValidator(regex, message="Invalid phone number entered!!", code="invalid_phone_no")])
    plan = models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True,related_name='patients')
    status = models.CharField(blank=False, null=False, choices=STATUS_CHOICES, default=ACTIVE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Patients'
        ordering=['-date_joined']

    def __str__(self):
        return self.name
    