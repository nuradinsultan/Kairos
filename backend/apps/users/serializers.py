from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import phonenumbers

from .models import (
    User,
    UserProfile,
    KYCDocument,
    Agreement,
    AuditLog
)
from .enums import (
    OnboardingStage,
    AccountType,
    UserRole,
    DocumentType,
    AgreementType
)

class PhoneNumberSerializer(serializers.Serializer):
    """
    Validates Ethiopian phone numbers
    """
    phone_number = serializers.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+251\d{9}$',
                message=_("Phone must be Ethiopian format: '+251xxxxxxxxx'.")
            )
        ]
    )

    def validate_phone_number(self, value):
        try:
            phone = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone):
                raise serializers.ValidationError(_("Invalid phone number"))
            if phonenumbers.region_code_for_number(phone) != 'ET':
                raise serializers.ValidationError(_("Only Ethiopian numbers allowed"))
            return value
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError(_("Invalid phone number format"))

class OTPSerializer(serializers.Serializer):
    """
    Validates OTP submissions
    """
    phone_number = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
            if not user.otp or user.otp != data['otp']:
                raise serializers.ValidationError(_("Invalid OTP"))
            if user.otp_expiry < timezone.now():
                raise serializers.ValidationError(_("OTP has expired"))
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Handles user profile data
    """
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'date_of_birth'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles new user registration with phone verification
    """
    profile = UserProfileSerializer(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'phone_number',
            'email',
            'role',
            'primary_account_type',
            'profile'
        ]
        extra_kwargs = {
            'phone_number': {'validators': [PhoneNumberSerializer().validate_phone_number]}
        }

    def validate_role(self, value):
        if value not in [UserRole.RETAIL_INVESTOR.value, UserRole.INSTITUTIONAL_INVESTOR.value]:
            raise serializers.ValidationError(
                _("Only retail or institutional investor roles allowed during registration")
            )
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

class OnboardingStatusSerializer(serializers.ModelSerializer):
    """
    Serializes onboarding progress
    """
    current_stage = serializers.SerializerMethodField()
    completed = serializers.BooleanField(source='is_onboarding_complete', read_only=True)

    class Meta:
        model = User
        fields = [
            'current_stage',
            'completed',
            'onboarding_data'
        ]
        read_only_fields = fields

    def get_current_stage(self, obj):
        return {
            'code': obj.onboarding_stage,
            'display': OnboardingStage(obj.onboarding_stage).label
        }

class KYCDocumentSerializer(serializers.ModelSerializer):
    """
    Handles KYC document upload and status
    """
    document_type_display = serializers.CharField(
        source='get_document_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = KYCDocument
        fields = [
            'id',
            'document_type',
            'document_type_display',
            'document_front',
            'document_back',
            'status',
            'status_display',
            'created_at',
            'reviewed_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'status_display',
            'created_at',
            'reviewed_at'
        ]

    def validate_document_type(self, value):
        if value not in dict(DocumentType.choices()):
            raise serializers.ValidationError(_("Invalid document type"))
        return value

class AgreementSerializer(serializers.ModelSerializer):
    """
    Handles e-signature agreements
    """
    agreement_type_display = serializers.CharField(
        source='get_agreement_type_display',
        read_only=True
    )

    class Meta:
        model = Agreement
        fields = [
            'id',
            'agreement_type',
            'agreement_type_display',
            'version',
            'content',
            'signed_at'
        ]
        read_only_fields = [
            'id',
            'content',
            'signed_at'
        ]

class AccountSwitchSerializer(serializers.Serializer):
    """
    Handles account switching between primary/secondary accounts
    """
    account_type = serializers.ChoiceField(choices=AccountType.choices())

    def validate_account_type(self, value):
        user = self.context['request'].user
        if value not in [user.primary_account_type] + user.secondary_account_types:
            raise serializers.ValidationError(
                _("You don't have access to this account type")
            )
        return value

class DemoAccountResetSerializer(serializers.Serializer):
    """
    Handles demo account balance reset
    """
    confirm = serializers.BooleanField(
        required=True,
        help_text=_("Must explicitly confirm reset")
    )

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError(
                _("You must confirm the reset")
            )
        return value

class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializes audit trail entries
    """
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user',
            'user_display',
            'action',
            'ip_address',
            'created_at'
        ]
        read_only_fields = fields

    def get_user_display(self, obj):
        return str(obj.user) if obj.user else "System"

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extended JWT serializer with additional user data
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        user = self.user
        data.update({
            'phone_number': user.phone_number,
            'is_verified': user.is_verified,
            'onboarding_stage': user.onboarding_stage,
            'active_account': user.active_account,
            'role': user.role
        })
        return data

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive user details serializer
    """
    profile = UserProfileSerializer(read_only=True)
    role_display = serializers.CharField(
        source='get_role_display',
        read_only=True
    )
    account_type_display = serializers.CharField(
        source='get_primary_account_type_display',
        read_only=True
    )
    active_account_display = serializers.CharField(
        source='get_active_account_display',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'email',
            'role',
            'role_display',
            'primary_account_type',
            'account_type_display',
            'secondary_account_types',
            'active_account',
            'active_account_display',
            'is_verified',
            'onboarding_stage',
            'profile'
        ]
        read_only_fields = fields
