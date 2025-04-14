from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, KYCDocument, Agreement

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle user creation and updates"""
    if created:
        from .services import OnboardingService
        OnboardingService.initiate_onboarding(instance)
        
    # Sync email verification status
    if instance.is_verified and instance.onboarding_stage == OnboardingStage.EMAIL_VERIFICATION.value:
        from .services import OnboardingService
        OnboardingService.progress_stage(instance, OnboardingStage.PHONE_VERIFICATION.value)

@receiver(post_save, sender=KYCDocument)
def kyc_document_post_save(sender, instance, created, **kwargs):
    """Handle KYC document updates"""
    if instance.status == KYCStatus.APPROVED.value:
        from .services import NotificationService
        NotificationService.send_kyc_approval(instance.user.phone_number)

@receiver(pre_save, sender=Agreement)
def agreement_pre_save(sender, instance, **kwargs):
    """Set agreement content before saving"""
    if not instance.content:
        from .services import DocumentService
        instance.content = DocumentService.generate_agreement(
            instance.agreement_type,
            instance.version
        )

@receiver(post_save, sender=Agreement)
def agreement_post_save(sender, instance, created, **kwargs):
    """Handle post-agreement signing"""
    if created:
        from .services import AuditService
        AuditService.log_action(
            user=instance.user,
            action=f"agreement_signed_{instance.agreement_type}",
            metadata={'version': instance.version}
        )
