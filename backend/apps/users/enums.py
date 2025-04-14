from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum

class OnboardingStage(models.TextChoices):
    EMAIL_VERIFICATION = 'email_verification', _('Email Verification')
    PHONE_VERIFICATION = 'phone_verification', _('Phone Verification')
    BASIC_INFO = 'basic_info', _('Basic Information')
    KYC_SUBMISSION = 'kyc_submission', _('KYC Submission')
    AGREEMENT_SIGNING = 'agreement_signing', _('Agreement Signing')
    COMPLETED = 'completed', _('Completed')

class UserRole(models.TextChoices):
    RETAIL_INVESTOR = 'retail_investor', _('Retail Investor')
    INSTITUTIONAL_INVESTOR = 'institutional_investor', _('Institutional Investor')
    BROKER = 'broker', _('Broker')
    TRADER = 'trader', _('Trader')
    REGULATOR = 'regulator', _('Regulator')
    COMPLIANCE_OFFICER = 'compliance_officer', _('Compliance Officer')
    SYSTEM_ADMIN = 'system_admin', _('System Administrator')

class AccountType(models.TextChoices):
    INDIVIDUAL = 'individual', _('Individual')
    CORPORATE = 'corporate', _('Corporate')
    JOINT = 'joint', _('Joint Account')
    DEMO = 'demo', _('Demo Account')

class KYCStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    UNDER_REVIEW = 'under_review', _('Under Review')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')

class DocumentType(models.TextChoices):
    NATIONAL_ID = 'national_id', _('National ID')
    PASSPORT = 'passport', _('Passport')
    DRIVERS_LICENSE = 'drivers_license', _("Driver's License")
    BUSINESS_LICENSE = 'business_license', _('Business License')

class AgreementType(models.TextChoices):
    TERMS_OF_SERVICE = 'terms_of_service', _('Terms of Service')
    PRIVACY_POLICY = 'privacy_policy', _('Privacy Policy')
    ELECTRONIC_COMMS = 'electronic_communications', _('Electronic Communications')
    RISK_DISCLOSURE = 'risk_disclosure', _('Risk Disclosure')

class NotificationType(Enum):
    OTP = 'otp'
    KYC_REMINDER = 'kyc_reminder'
    ACCOUNT_APPROVAL = 'account_approval'
    TRADE_CONFIRMATION = 'trade_confirmation'
