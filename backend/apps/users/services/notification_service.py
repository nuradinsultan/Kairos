import requests
from django.conf import settings

class SMSNotificationService:
    @staticmethod
    def send_otp(phone_number, otp):
        """
        Send OTP via SMS (Telebirr integration example)
        """
        if settings.DEBUG:
            print(f"OTP for {phone_number}: {otp}")
            return True
            
        payload = {
            "recipient": phone_number,
            "message": f"Your verification code is: {otp}",
            "sender_id": settings.SMS_SENDER_ID
        }
        
        try:
            response = requests.post(
                settings.SMS_API_URL,
                json=payload,
                headers={'Authorization': f'Bearer {settings.SMS_API_KEY}'}
            )
            return response.status_code == 200
        except Exception as e:
            # Log error
            return False

    @staticmethod
    def send_kyc_reminder(phone_number):
        """
        Send KYC submission reminder
        """
        message = "Please submit your KYC documents to complete registration"
        return SMSNotificationService._send_sms(phone_number, message)

    @staticmethod
    def _send_sms(phone_number, message):
        """Generic SMS sending method"""
        if settings.DEBUG:
            print(f"SMS to {phone_number}: {message}")
            return True
            
        # Actual SMS gateway integration
        # ...
