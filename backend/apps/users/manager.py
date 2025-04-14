from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .constants import ETHIOPIAN_COUNTRY_CODE
import random
from datetime import timedelta
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _validate_phone_number(self, phone_number):
        """Validate Ethiopian phone number format"""
        if not phone_number.startswith(ETHIOPIAN_COUNTRY_CODE):
            raise ValueError(_('Phone number must start with +251'))
        return phone_number

    def _create_user(self, phone_number, email, password=None, **extra_fields):
        """Core user creation logic"""
        if not phone_number:
            raise ValueError(_('Phone number must be set'))
        
        phone_number = self._validate_phone_number(phone_number)
        email = self.normalize_email(email) if email else None
        
        user = self.model(
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        """Create regular user with OTP verification"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self._create_user(phone_number, email, password, **extra_fields)
        user.generate_otp()
        return user

    def create_superuser(self, phone_number, email, password, **extra_fields):
        """Create superuser with bypassed verification"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', UserRole.SYSTEM_ADMIN.value)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
            
        return self._create_user(phone_number, email, password, **extra_fields)

    def get_by_natural_key(self, phone_number):
        """Allow login with phone number"""
        return self.get(phone_number=phone_number)
