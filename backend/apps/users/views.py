from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from .models import User, UserProfile, KYCDocument, Agreement
from .serializers import (
    PhoneNumberSerializer,
    OTPSerializer,
    UserRegistrationSerializer,
    OnboardingStatusSerializer,
    KYCDocumentSerializer,
    AgreementSerializer,
    AccountSwitchSerializer,
    DemoAccountResetSerializer,
    CustomTokenObtainPairSerializer,
    UserDetailSerializer
)
from .services import (
    AuthService,
    OnboardingService,
    KYCService,
    DocumentService
)
from .permissions import (
    IsEthiopianUser,
    IsOnboardingStage,
    HasAccountType,
    IsVerifiedUser
)

# ==============================================
# AUTHENTICATION VIEWS
# ==============================================

@method_decorator([never_cache, csrf_protect], name='dispatch')
class RequestOTPView(generics.GenericAPIView):
    """
    Initiate OTP process for phone verification
    """
    serializer_class = PhoneNumberSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        success = AuthService.send_otp(phone_number)
        
        if not success:
            return Response(
                {"detail": "Failed to send OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        return Response({
            "status": "OTP sent",
            "phone_number": phone_number
        })

@method_decorator([never_cache, csrf_protect], name='dispatch')
class VerifyOTPView(generics.GenericAPIView):
    """
    Verify OTP and activate user
    """
    serializer_class = OTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        user = get_object_or_404(User, phone_number=phone_number)
        
        if user.verify_otp(serializer.validated_data['otp']):
            return Response({
                "status": "verified",
                "phone_number": phone_number
            })
        return Response(
            {"detail": "Invalid OTP or expired"},
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login with additional user data
    """
    serializer_class = CustomTokenObtainPairSerializer

# ==============================================
# USER REGISTRATION & PROFILE
# ==============================================

class UserRegistrationView(generics.CreateAPIView):
    """
    Complete user registration after phone verification
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        OnboardingService.initiate_onboarding(user)
        
        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Manage user profile data
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def get_object(self):
        return self.request.user

# ==============================================
# ONBOARDING FLOW VIEWS
# ==============================================

class OnboardingStatusView(generics.RetrieveAPIView):
    """
    Check current onboarding status
    """
    serializer_class = OnboardingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class KYCDocumentUploadView(generics.CreateAPIView):
    """
    Upload KYC documents for verification
    """
    serializer_class = KYCDocumentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOnboardingStage(OnboardingStage.KYC_SUBMISSION)
    ]

    def perform_create(self, serializer):
        document = serializer.save(user=self.request.user)
        KYCService.process_document_async(document.id)
        OnboardingService.progress_stage(
            self.request.user,
            OnboardingStage.AGREEMENT_SIGNING.value
        )

class AgreementSignView(generics.CreateAPIView):
    """
    E-sign legal agreements
    """
    serializer_class = AgreementSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOnboardingStage(OnboardingStage.AGREEMENT_SIGNING)
    ]

    def perform_create(self, serializer):
        agreement = serializer.save(
            user=self.request.user,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        OnboardingService.progress_stage(
            self.request.user,
            OnboardingStage.COMPLETED.value
        )
        return agreement

# ==============================================
# ACCOUNT MANAGEMENT
# ==============================================

class AccountSwitchView(generics.GenericAPIView):
    """
    Switch between primary/secondary accounts
    """
    serializer_class = AccountSwitchSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        success = request.user.switch_active_account(
            serializer.validated_data['account_type']
        )
        
        if not success:
            return Response(
                {"detail": "Account switching failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response({
            "status": "account_switched",
            "active_account": request.user.active_account
        })

class DemoAccountResetView(generics.GenericAPIView):
    """
    Reset demo account balance
    """
    serializer_class = DemoAccountResetSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsVerifiedUser,
        HasAccountType(AccountType.DEMO)
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            request.user.reset_demo_balance()
            return Response({
                "status": "balance_reset",
                "new_balance": request.user.demo_balance
            })
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# ==============================================
# ADMIN & COMPLIANCE VIEWS
# ==============================================

class KYCDocumentReviewView(generics.UpdateAPIView):
    """
    Admin view for KYC document review
    """
    queryset = KYCDocument.objects.all()
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        document = serializer.save(reviewed_at=timezone.now())
        if document.status == KYCStatus.APPROVED.value:
            DocumentService.approve_user_documents(document.user)

class UserListView(generics.ListAPIView):
    """
    Admin view for user management
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().select_related('profile')
    filterset_fields = ['role', 'is_verified', 'onboarding_stage']
    search_fields = ['phone_number', 'email', 'profile__first_name', 'profile__last_name']
    ordering_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']
