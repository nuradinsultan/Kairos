# backend/apps/user_profiles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile, KYC
from .forms import UserProfileForm, KYCForm

@login_required
def user_profile(request):
    """View to display and update the user's profile."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'user_profiles/user_profile.html', {'form': form})


@login_required
def kyc_submission(request):
    """View for submitting and updating KYC documents."""
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None
    
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.save()
            messages.success(request, "KYC documents submitted successfully. Awaiting verification.")
            return redirect('kyc_submission')
    else:
        form = KYCForm(instance=kyc)
    
    return render(request, 'user_profiles/kyc_submission.html', {'form': form})


@login_required
def kyc_verification(request):
    """View to handle KYC verification status and update."""
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None
    
    if request.method == 'POST':
        if kyc:
            kyc.verified = True
            kyc.save()
            messages.success(request, "KYC verification complete.")
        else:
            messages.error(request, "KYC details not found.")
        return redirect('kyc_verification')
    
    return render(request, 'user_profiles/kyc_verification.html', {'kyc': kyc})


def kyc_status(request):
    """API endpoint to get KYC verification status."""
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
            return JsonResponse({'verified': kyc.verified})
        except KYC.DoesNotExist:
            return JsonResponse({'error': 'KYC details not found'}, status=404)
    return JsonResponse({'error': 'User not authenticated'}, status=401)
