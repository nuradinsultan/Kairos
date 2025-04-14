import phonenumbers
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, identifier, password, **extra_fields):
        """
        Create and save a user with the given identifier (email or phone) and password.
        """
        if not identifier:
            raise ValueError('Users must have an email or phone number')
        
        # Normalize identifier
        if '@' in identifier:
            identifier = self.normalize_email(identifier)
            extra_fields.setdefault('email', identifier)
        else:
            if not identifier.startswith('+251'):
                raise ValueError('Only Ethiopian phone numbers (+251) are allowed')
            extra_fields.setdefault('phone_number', identifier)
        
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(identifier, password, **extra_fields)

def validate_ethiopian_phone(value):
    """Strict validation for Ethiopian phone numbers"""
    try:
        phone = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError(_("Invalid phone number"))
        if phonenumbers.region_code_for_number(phone) != 'ET':
            raise ValidationError(_("Only Ethiopian phone numbers (+251) are allowed"))
    except phonenumbers.NumberParseException:
        raise ValidationError(_("Phone number must be in format: +251XXXXXXXXX"))

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required if not using phone number')
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_ethiopian_phone],
        help_text=_('Ethiopian phone number (+251XXXXXXXXX)')
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
    REQUIRED_FIELDS = []  # Email/phone handled separately

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
        """Return the primary contact identifier (email or phone)"""
        return self.email if self.email else self.phone_number
