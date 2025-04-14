from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RequestOTPView,
    VerifyOTPView,
    CustomTokenObtainPairView,
    UserRegistrationView,
    UserProfileView,
    OnboardingStatusView,
    KYCDocumentUploadView,
    AgreementSignView,
    AccountSwitchView,
    DemoAccountResetView,
    KYCDocumentReviewView,
    UserListView
)

app_name = 'users'

# Router for viewset endpoints
router = DefaultRouter(trailing_slash=False)
# router.register('some-viewset', SomeViewSet)  # Example for viewset registration

urlpatterns = [
    # Authentication Endpoints
    path('auth/request-otp', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Registration & Profile
    path('register', UserRegistrationView.as_view(), name='register'),
    path('profile', UserProfileView.as_view(), name='profile'),
    
    # Onboarding Flow
    path('onboarding/status', OnboardingStatusView.as_view(), name='onboarding-status'),
    path('onboarding/kyc', KYCDocumentUploadView.as_view(), name='kyc-upload'),
    path('onboarding/agreements', AgreementSignView.as_view(), name='agreement-sign'),
    
    # Account Management
    path('accounts/switch', AccountSwitchView.as_view(), name='account-switch'),
    path('accounts/demo/reset', DemoAccountResetView.as_view(), name='demo-reset'),
    
    # Admin Endpoints
    path('admin/kyc/<uuid:pk>', KYCDocumentReviewView.as_view(), name='kyc-review'),
    path('admin/users', UserListView.as_view(), name='user-list'),
    
    # Include router URLs
    path('', include(router.urls)),
]
