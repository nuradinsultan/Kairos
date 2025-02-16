# backend/apps/trading/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Order, Trade, Stock
from .forms import OrderForm

@login_required
def place_order(request):
    """View to place an order (buy or sell)."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Order placed successfully.")
            return redirect('order_history')
    else:
        form = OrderForm()

    return render(request, 'trading/place_order.html', {'form': form})


@login_required
def execute_trade(order):
    """Function to match buy and sell orders and execute trades."""
    if order.status != 'Pending':
        return None  # Trade can only be executed if the order is pending

    if order.order_type == 'buy':
        matching_order = Order.objects.filter(stock=order.stock, order_type='sell', status='Pending').first()
        if matching_order:
            executed_quantity = min(order.quantity, matching_order.quantity)
            executed_price = matching_order.price_per_unit  # Matching price from the sell order

            # Create trade for this matched order
            trade = Trade.objects.create(
                order=order,
                executed_price=executed_price,
                executed_quantity=executed_quantity,
                executed_at=timezone.now(),
            )

            # Update the orders
