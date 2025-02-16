# backend/apps/payment/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PaymentMethod(models.Model):
    """Model to define different payment methods available for users."""
    name = models.CharField(max_length=100, unique=True)  # e.g., 'Credit Card', 'Bank Transfer'
    description = models.TextField(blank=True, null=True)  # Description of the payment method
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PaymentStatus(models.Model):
    """Model to track different payment statuses."""
    status = models.CharField(max_length=100, unique=True)  # e.g., 'Pending', 'Completed', 'Failed', 'Refunded'
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.status


class PaymentTransaction(models.Model):
    """Model to record individual payment transactions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)  # Payment method used
    status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True)  # Payment status
    transaction_reference = models.CharField(max_length=255, unique=True)  # Unique transaction reference
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of the transaction
    updated_at = models.DateTimeField(auto_now=True)  # Last update time
    payment_date = models.DateTimeField(null=True, blank=True)  # Actual payment date (when it's processed)

    def __str__(self):
        return f"Transaction {self.transaction_reference} - {self.user.username}"

    def mark_as_paid(self):
        """Mark the payment as completed and update the payment date."""
        self.status = PaymentStatus.objects.get(status="Completed")
        self.payment_date = timezone.now()
        self.save()

    def mark_as_failed(self):
        """Mark the payment as failed."""
        self.status = PaymentStatus.objects.get(status="Failed")
        self.save()

    def mark_as_refunded(self):
        """Mark the payment as refunded."""
        self.status = PaymentStatus.objects.get(status="Refunded")
        self.save()


class RefundTransaction(models.Model):
    """Model to track refund transactions."""
    original_transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='refunds')
    amount_refunded = models.DecimalField(max_digits=10, decimal_places=2)
    refund_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)  # Reason for the refund

    def __str__(self):
        return f"Refund for {self.original_transaction.transaction_reference}"
