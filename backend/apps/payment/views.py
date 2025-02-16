# backend/apps/payment/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import PaymentTransaction, PaymentMethod, PaymentStatus, RefundTransaction
from .forms import PaymentTransactionForm  # You can create a form for payments if needed
from django.conf import settings
import logging

# Initialize logger
logger = logging.getLogger(__name__)

@login_required
def initiate_payment(request):
    """
    View to initiate a payment transaction for a logged-in user.
    It provides the payment methods to the user and processes the payment.
    """
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        try:
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            amount = float(amount)

            # Create the PaymentTransaction
            payment_transaction = PaymentTransaction.objects.create(
                user=request.user,
                amount=amount,
                payment_method=payment_method,
                status=PaymentStatus.objects.get(status='Pending'),
                transaction_reference="TXN" + str(int(timezone.now().timestamp())),  # Unique transaction ref
                created_at=timezone.now(),
            )

            # Process the payment through external payment gateway
            # Here, you would integrate with a real payment gateway (e.g., Stripe, PayPal)
            # For now, we simulate successful payment processing

            # Simulate payment success for now
            payment_transaction.mark_as_paid()

            # After successful payment, redirect to success page or send success response
            return redirect('payment:payment_success', transaction_id=payment_transaction.id)
        except PaymentMethod.DoesNotExist:
            logger.error(f"Invalid payment method selected by user {request.user.username}")
            return JsonResponse({"error": "Invalid payment method selected."}, status=400)
        except Exception as e:
            logger.error(f"Error initiating payment: {str(e)}")
            return JsonResponse({"error": "An error occurred while processing the payment."}, status=500)

    # If GET request, show available payment methods
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'payment/initiate_payment.html', {'payment_methods': payment_methods})


@login_required
def payment_success(request, transaction_id):
    """
    View to display the success page after payment is processed.
    """
    try:
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        if transaction.user == request.user:
            return render(request, 'payment/payment_success.html', {'transaction': transaction})
        else:
            return redirect('payment:payment_failed')
    except PaymentTransaction.DoesNotExist:
        return redirect('payment:payment_failed')


@login_required
def payment_failed(request):
    """
    View to display the failure page if a payment did not complete successfully.
    """
    return render(request, 'payment/payment_failed.html')


@login_required
def transaction_history(request):
    """
    View to display a user's payment transaction history.
    """
    transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payment/transaction_history.html', {'transactions': transactions})


@login_required
def process_refund(request, transaction_id):
    """
    View to process a refund for a payment transaction.
    """
    try:
        transaction = PaymentTransaction.objects.get(id=transaction_id)

        if transaction.user != request.user:
            return JsonResponse({"error": "You cannot refund another user's transaction."}, status=403)

        if transaction.status.status != "Completed":
            return JsonResponse({"error": "Only completed payments can be refunded."}, status=400)

        # Create a refund transaction record
        refund = RefundTransaction.objects.create(
            original_transaction=transaction,
            amount_refunded=transaction.amount,
            reason=request.POST.get('reason', 'No reason provided'),
        )

        # Mark the original transaction as refunded
        transaction.mark_as_refunded()

        # Optionally: Call external payment gateway API to process the actual refund
        # For now, we're simulating a successful refund
        logger.info(f"Refund successful for transaction {transaction.transaction_reference}.")

        return JsonResponse({"message": "Refund processed successfully.", "refund_id": refund.id}, status=200)

    except PaymentTransaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found."}, status=404)
    except Exception as e:
        logger.error(f"Error processing refund: {str(e)}")
        return JsonResponse({"error": "An error occurred while processing the refund."}, status=500)
