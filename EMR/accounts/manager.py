from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            validate_email(email)
        else:
            raise ValueError(_("Please provide an email address"))
        
        if not full_name:
            raise ValueError(_("Please provide a Full name"))

        user= self.model(email=email, full_name= full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Admin user must have this specified as true"))
        
        if extra_fields.get('is_superuser') is not False:
            raise ValueError(_("Admin user should not have superadmin privileges"))
        
        return self.create_user(email=email, full_name=full_name, password=password, **extra_fields)
        # user.save(using=self._db)
        # return user
    
    def create_superuser(self, email, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superadmin user must have this specified as true"))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superadmin user should have superadmin privileges"))
        
        return self.create_user(email=email, full_name=full_name, password=password, **extra_fields)
