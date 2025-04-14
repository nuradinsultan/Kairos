from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from .enums import OnboardingStage, UserRole, AccountType

class IsEthiopianUser(permissions.BasePermission):
    """Verify user has an Ethiopian phone number"""
    message = "Only Ethiopian phone numbers are allowed"

    def has_permission(self, request, view):
        return request.user.phone_number.startswith('+251')

class IsOnboardingStage(permissions.BasePermission):
    """Check if user is at specific onboarding stage"""
    def __init__(self, required_stage):
        self.required_stage = required_stage

    def has_permission(self, request, view):
        return request.user.onboarding_stage == self.required_stage.value

class HasUserRole(permissions.BasePermission):
    """Check if user has specific role"""
    def __init__(self, allowed_roles):
        self.allowed_roles = [role.value if hasattr(role, 'value') else role for role in allowed_roles]

    def has_permission(self, request, view):
        return request.user.role in self.allowed_roles

class HasAccountType(permissions.BasePermission):
    """Verify user has access to specific account type"""
    def __init__(self, account_type):
        self.account_type = account_type.value if hasattr(account_type, 'value') else account_type

    def has_permission(self, request, view):
        user = request.user
        return (user.primary_account_type == self.account_type or 
                self.account_type in user.secondary_account_types)

class IsVerifiedUser(permissions.BasePermission):
    """Check if user completed verification"""
    def has_permission(self, request, view):
        if not request.user.is_verified:
            raise PermissionDenied("Account verification required")
        return True

class CanTrade(permissions.BasePermission):
    """Check if user has trading permissions"""
    def has_permission(self, request, view):
        user = request.user
        return (user.is_verified and 
                user.onboarding_stage == OnboardingStage.COMPLETED.value and
                user.role in [UserRole.RETAIL_INVESTOR.value, 
                             UserRole.INSTITUTIONAL_INVESTOR.value])
