from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import phonenumbers

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    # Ethiopia country code validation
    ETHIOPIA_COUNTRY_CODE = 'ET'
    phone_regex = RegexValidator(
        regex=r'^\+251\d{9}$',
        message="Ethiopian phone number must be in format: +251XXXXXXXXX"
    )
    phone_number = models.CharField(
        max_length=13,  # +251 + 9 digits
        unique=True,
        validators=[phone_regex]
    )
    
    def clean(self):
        super().clean()
        try:
            phone = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError("Invalid phone number")
                
            country_code = phonenumbers.region_code_for_number(phone)
            if country_code != self.ETHIOPIA_COUNTRY_CODE:
                raise ValidationError(
                    f"Only Ethiopian phone numbers (+251) are allowed"
                )
                
        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid phone number format")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email
