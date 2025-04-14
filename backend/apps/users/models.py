import uuid
import phonenumbers
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .managers import CustomUserManager
from .enums import (
    OnboardingStage,
    AccountType,
    UserRole,
    KYCStatus,
    AgreementType,
    DocumentType
)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with Ethiopian phone verification and comprehensive financial features
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ======================
    # AUTHENTICATION FIELDS
    # ======================
    phone_regex = RegexValidator(
        regex=r'^\+251\d{9}$',
        message=_("Phone must be Ethiopian format: '+251xxxxxxxxx'.")
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=13,
        unique=True,
        validators=[phone_regex]
    )
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    
    # ==================
    # SECURITY FIELDS
    # ==================
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    pin = models.CharField(_('transaction PIN'), max_length=6, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    
    # ======================
    # ONBOARDING PROGRESS
    # ======================
    onboarding_stage = models.CharField(
        _('onboarding stage'),
        max_length=20,
        choices=OnboardingStage.choices(),
        default=OnboardingStage.EMAIL_VERIFICATION.value
    )
    onboarding_data = models.JSONField(_('onboarding data'), default=dict, blank=True)
    
    # ======================
    # ACCOUNT CONFIGURATION
    # ======================
    role = models.CharField(
        _('role'),
        max_length=22,
        choices=UserRole.choices(),
        default=UserRole.RETAIL_INVESTOR.value
    )
    primary_account_type = models.CharField(
        _('primary account type'),
        max_length=10,
        choices=AccountType.choices(),
        default=AccountType.INDIVIDUAL.value
    )
    secondary_account_types = ArrayField(
        models.CharField(max_length=10, choices=AccountType.choices()),
        default=list,
        blank=True
    )
    active_account = models.CharField(
        _('active account'),
        max_length=10,
        choices=AccountType.choices(),
        default=AccountType.INDIVIDUAL.value
    )
    
    # ======================
    # DEMO ACCOUNT FEATURES
    # ======================
    demo_balance = models.DecimalField(
        _('demo balance'),
        max_digits=15,
        decimal_places=2,
        default=100000.00,
        validators=[MinValueValidator(0)]
    )
    demo_reset_count = models.PositiveIntegerField(_('demo resets'), default=0)
    last_demo_reset = models.DateTimeField(_('last demo reset'), null=True, blank=True)
    
    # ======================
    # TIMESTAMPS
    # ======================
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['onboarding_stage']),
            models.Index(fields=['active_account']),
        ]

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"

    def clean(self):
        """Validate Ethiopian phone number and account consistency"""
        super().clean()
        
        # Phone number validation
        try:
            phone = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError(_("Invalid phone number"))
            if phonenumbers.region_code_for_number(phone) != 'ET':
                raise ValidationError(_("Only Ethiopian numbers allowed"))
        except phonenumbers.NumberParseException:
            raise ValidationError(_("Invalid phone number format"))
        
        # Account type validation
        if self.active_account not in [self.primary_account_type] + self.secondary_account_types:
            raise ValidationError(_("Active account must be primary or secondary account type"))

    # ======================
    # OTP METHODS
    # ======================
    def generate_otp(self):
        """Generate and save a 6-digit OTP valid for 5 minutes"""
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        self.save()
        return self.otp

    def verify_otp(self, otp):
        """Verify provided OTP and mark user as verified if valid"""
        if self.otp == otp and self.otp_expiry > timezone.now():
            self.is_verified = True
            self.otp = None
            self.otp_expiry = None
            self.save()
            return True
        return False

    # ======================
    # ONBOARDING METHODS
    # ======================
    def send_verification_email(self):
        """Send email verification link"""
        if not self.email:
            raise ValueError("User has no email address configured")
        
        context = {
            'user': self,
            'verification_url': (
                f"{settings.FRONTEND_URL}/verify-email/"
                f"{self.id}/{self.email_verification_token}/"
            )
        }
        
        send_mail(
            subject=_('Verify Your Email'),
            message=render_to_string('emails/verification.txt', context),
            html_message=render_to_string('emails/verification.html', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False
        )

    def progress_onboarding(self, new_stage):
        """Progress user to next onboarding stage if valid"""
        current_stage = OnboardingStage(self.onboarding_stage)
        new_stage = OnboardingStage(new_stage)
        
        if new_stage.value > current_stage.value:
            self.onboarding_stage = new_stage.value
            self.save()
            return True
        return False

    # ======================
    # DEMO ACCOUNT METHODS
    # ======================
    def reset_demo_balance(self):
        """Reset demo account balance to initial value"""
        if self.active_account != AccountType.DEMO.value:
            raise ValueError("Can only reset demo account balance")
        
        self.demo_balance = 100000.00
        self.demo_reset_count += 1
        self.last_demo_reset = timezone.now()
        self.save()

    # ======================
    # ACCOUNT MANAGEMENT
    # ======================
    def add_secondary_account(self, account_type):
        """Add a secondary account type if not already present"""
        if account_type not in self.secondary_account_types:
            self.secondary_account_types.append(account_type)
            self.save()

    def switch_active_account(self, account_type):
        """Switch active account if available to user"""
        if account_type in [self.primary_account_type] + self.secondary_account_types:
            self.active_account = account_type
            self.save()
            return True
        return False


class UserProfile(models.Model):
    """
    Extended user profile information
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class KYCDocument(models.Model):
    """
    KYC document submission and processing
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='kyc_documents'
    )
    document_type = models.CharField(
        _('document type'),
        max_length=20,
        choices=DocumentType.choices()
    )
    document_front = models.FileField(
        _('document front'),
        upload_to='kyc/'
    )
    document_back = models.FileField(
        _('document back'),
        upload_to='kyc/',
        blank=True,
        null=True
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=KYCStatus.choices(),
        default=KYCStatus.PENDING.value
    )
    metadata = models.JSONField(_('metadata'), default=dict)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    reviewed_at = models.DateTimeField(_('reviewed at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('KYC document')
        verbose_name_plural = _('KYC documents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.phone_number} - {self.get_document_type_display()}"


class Agreement(models.Model):
    """
    E-signature agreements tracking
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agreements'
    )
    agreement_type = models.CharField(
        _('agreement type'),
        max_length=50,
        choices=AgreementType.choices()
    )
    version = models.CharField(_('version'), max_length=20)
    content = models.TextField(_('content'))
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('user agent'))
    signed_at = models.DateTimeField(_('signed at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('agreement')
        verbose_name_plural = _('agreements')
        unique_together = ('user', 'agreement_type', 'version')
        ordering = ['-signed_at']

    def __str__(self):
        return f"{self.user.phone_number} - {self.agreement_type} v{self.version}"


class AuditLog(models.Model):
    """
    Audit trail for sensitive user actions
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(_('action'), max_length=50)
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('user agent'), blank=True)
    metadata = models.JSONField(_('metadata'), default=dict)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('audit log')
        verbose_name_plural = _('audit logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user.phone_number if self.user else 'System'} - {self.action}"
