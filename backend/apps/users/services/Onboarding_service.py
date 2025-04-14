from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from ..models import User
from ..enums import OnboardingStage

class OnboardingService:
    @classmethod
    def initiate_onboarding(cls, user):
        """
        Start onboarding process with email verification
        """
        cls.send_verification_email(user)
        user.onboarding_stage = OnboardingStage.EMAIL_VERIFICATION.value
        user.save()

    @classmethod
    def send_verification_email(cls, user):
        """
        Send email verification link
        """
        context = {
            'user': user,
            'verification_url': f"{settings.FRONTEND_URL}/verify-email/{user.id}/"
        }
        
        send_mail(
            subject='Verify Your Email',
            message=render_to_string('emails/verification.txt', context),
            html_message=render_to_string('emails/verification.html', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

    @classmethod
    def progress_stage(cls, user, new_stage):
        """
        Move user to next onboarding stage if valid transition
        """
        current = OnboardingStage(user.onboarding_stage)
        new = OnboardingStage(new_stage)
        
        if new.value > current.value:
            user.onboarding_stage = new.value
            user.save()
            
            # Trigger stage-specific actions
            if new == OnboardingStage.KYC_SUBMISSION:
                from .notification_service import SMSNotificationService
                SMSNotificationService.send_kyc_reminder(user.phone_number)
            
            return True
        return False

    @classmethod
    def is_onboarding_complete(cls, user):
        """
        Check if user has completed all onboarding stages
        """
        return user.onboarding_stage == OnboardingStage.COMPLETED.value
