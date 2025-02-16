# backend/apps/user_profiles/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class KYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="kyc")
    full_name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=255, unique=True)
    id_type = models.CharField(max_length=50, choices=[('National ID', 'National ID'), ('Passport', 'Passport'), ('Driver License', 'Driver License')])
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()
    verified = models.BooleanField(default=False)  # KYC verification status
    address_proof = models.FileField(upload_to="kyc_address_proofs/", blank=True, null=True)
    id_proof = models.FileField(upload_to="kyc_id_proofs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC for {self.user.username}"

    class Meta:
        verbose_name = _("KYC Document")
        verbose_name_plural = _("KYC Documents")
