import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from ..models import User

class AuthService:
    @classmethod
    def send_otp(cls, phone_number):
        """
        Generate and send OTP to Ethiopian phone number
        Returns True if successful
        """
        try:
            user, created = User.objects.get_or_create(phone_number=phone_number)
            otp = cls._generate_otp()
            expiry = timezone.now() + timedelta(minutes=5)
            
            user.otp = otp
            user.otp_expiry = expiry
            user.save()
            
            if not settings.DEBUG:
                from .notification_service import SMSNotificationService
                SMSNotificationService.send_otp(phone_number, otp)
            
            return True
        except Exception as e:
            # Log error
            return False

    @staticmethod
    def _generate_otp():
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))

    @classmethod
    def verify_phone_number(cls, phone_number, otp):
        """
        Verify OTP for Ethiopian phone number
        Returns User object if verified, None otherwise
        """
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.otp == otp and user.otp_expiry > timezone.now():
                user.is_verified = True
                user.otp = None
                user.otp_expiry = None
                user.save()
                return user
        except User.DoesNotExist:
            pass
        return None

    @classmethod
    def complete_registration(cls, user, profile_data):
        """
        Complete user registration after phone verification
        """
        from ..models import UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults=profile_data
        )
        return user
