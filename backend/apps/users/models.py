import phonenumbers
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, identifier, password=None, **extra_fields):
        if not identifier:
            raise ValueError('User must have either email or phone number')
        
        email = None
        phone_number = None
        
        if '@' in identifier:
            email = self.normalize_email(identifier)
            extra_fields.setdefault('email', email)
        else:
            if not identifier.startswith('+251'):
                raise ValueError('Only Ethiopian phone numbers (+251) allowed')
            phone_number = identifier
            extra_fields.setdefault('phone_number', phone_number)
        
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(identifier, password, **extra_fields)

    def create_superuser(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(identifier, password, **extra_fields)

def validate_ethiopian_phone(value):
    try:
        phone = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Invalid phone number")
        if phonenumbers.region_code_for_number(phone) != 'ET':
            raise ValidationError("Only Ethiopian phone numbers (+251) allowed")
    except phonenumbers.NumberParseException:
        raise ValidationError("Phone number must be in format: +251XXXXXXXXX")

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=True,
        null=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_ethiopian_phone],
        error_messages={
            'unique': _('A user with that phone number already exists.'),
        },
    )
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )
    
    # Status fields
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    
    # Timestamps
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            raise ValidationError(_('User must have either an email or phone number'))
        
        if self.phone_number:
            validate_ethiopian_phone(self.phone_number)

    def get_identifier(self):
        return self.email if self.email else self.phone_number
