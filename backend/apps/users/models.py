import phonenumbers
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Best Practice: Isolate manager class
class CustomUserManager(BaseUserManager):
    """Best Practice: Document all methods"""
    
    def _validate_creation_fields(self, identifier: str) -> tuple[str, str]:
        """Validate email/phone and return normalized values"""
        email, phone = None, None
        
        if '@' in identifier:
            email = self.normalize_email(identifier)
            if not email:
                raise ValueError('Invalid email format')
        else:
            if not identifier.startswith('+251'):
                raise ValueError('Only Ethiopian (+251) numbers allowed')
            try:
                phone = phonenumbers.parse(identifier, None)
                if not phonenumbers.is_valid_number(phone):
                    raise ValueError('Invalid phone number')
                phone = phonenumbers.format_number(
                    phone, 
                    phonenumbers.PhoneNumberFormat.E164
                )
            except phonenumbers.NumberParseException as e:
                raise ValueError(f'Phone validation failed: {str(e)}')
        
        return email, phone or identifier

    def create_user(self, identifier: str, password: str = None, **extra_fields):
        """Best Practice: Type hints and docstrings"""
        if not identifier:
            raise ValueError('Identifier (email/phone) required')
            
        email, phone = self._validate_creation_fields(identifier)
        
        # Best Practice: Explicit field setting
        user = self.model(
            email=email,
            phone_number=phone,
            **extra_fields
        )
        
        # Best Practice: Password validation
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier: str, password: str, **extra_fields):
        """Best Practice: Explicit permission flags"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
            
        return self.create_user(identifier, password, **extra_fields)

# Best Practice: Separate validator functions
def validate_ethiopian_phone(value: str) -> None:
    """Production-grade phone validation"""
    try:
        phone = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError(
                _('%(value)s is not a valid phone number'),
                params={'value': value},
            )
        if phonenumbers.region_code_for_number(phone) != 'ET':
            raise ValidationError(
                _('Only Ethiopian (+251) numbers are allowed'),
                code='invalid_region'
            )
    except phonenumbers.NumberParseException as e:
        raise ValidationError(
            _('Invalid phone format: %(error)s'),
            params={'error': str(e)},
            code='invalid_format'
        )

class User(AbstractBaseUser, PermissionsMixin):
    """Best Practice: Comprehensive field definitions"""
    
    # Contact Fields
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text=_('User email address'),
        error_messages={
            'unique': _('This email is already registered'),
        },
        db_index=True  # Best Practice: Index frequently queried fields
    )
    
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_ethiopian_phone],
        help_text=_('Ethiopian number in E.164 format (+251XXXXXXXXX)'),
        error_messages={
            'unique': _('This phone number is already registered'),
        },
        db_index=True
    )
    
    # Auth Fields
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_(
            'Required. 30 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': _('This username is already taken'),
        },
    )
    
    # Status Fields
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active')
    )
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site')
    )
    
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether the user has completed verification')
    )
    
    # Timestamps
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
        editable=False
    )
    
    last_login = models.DateTimeField(
        _('last login'),
        auto_now=True,
        editable=False
    )
    
    # Best Practice: Define choices for future extensibility
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('am', 'Amharic'),
    ]
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']  # Best Practice: Default ordering
        indexes = [  # Best Practice: Composite indexes
            models.Index(fields=['email', 'phone_number']),
        ]

    def __str__(self) -> str:
        return self.username

    def clean(self) -> None:
        """Best Practice: Comprehensive validation"""
        super().clean()
        
        if not self.email and not self.phone_number:
            raise ValidationError(
                _('User must have either email or phone number'),
                code='missing_contact'
            )
            
        if self.phone_number:
            validate_ethiopian_phone(self.phone_number)

    def get_full_name(self) -> str:
        """Best Practice: Standard user method implementation"""
        return self.username

    def get_short_name(self) -> str:
        """Best Practice: Standard user method implementation"""
        return self.username.split('@')[0] if '@' in self.username else self.username

    @property
    def contact_info(self) -> str:
        """Best Practice: Business logic as properties"""
        return self.email or self.phone_number
