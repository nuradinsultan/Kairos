# backend/apps/trading/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Stock(models.Model):
    """Model representing a stock in the market."""
    symbol = models.CharField(max_length=10, unique=True)  # Stock symbol (e.g., 'AAPL')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)  # Current market price
    market_cap = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Market capitalization

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['symbol']


class Order(models.Model):
    """Model representing an order in the market."""
    BUY = 'buy'
    SELL = 'sell'
    ORDER_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField()  # Number of shares
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)  # Price per share
    status = models.CharField(max_length=15, default='Pending')  # Pending, Completed, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_type.capitalize()} {self.quantity} {self.stock.symbol} at {self.price_per_unit}"

    class Meta:
        ordering = ['-created_at']


class Trade(models.Model):
    """Model representing a trade execution."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='trade')
    executed_price = models.DecimalField(max_digits=12, decimal_places=2)  # Price at which the trade was executed
    executed_quantity = models.PositiveIntegerField()  # Number of shares exchanged
    executed_at = models.DateTimeField(default=timezone.now)  # Time when the trade was executed
    total_value = models.DecimalField(max_digits=18, decimal_places=2)  # Total trade value (price * quantity)

    def save(self, *args, **kwargs):
        # Calculate total value for the trade before saving
        self.total_value = self.executed_price * self.executed_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trade {self.order.id}: {self.executed_quantity} {self.order.stock.symbol} at {self.executed_price}"

    class Meta:
        ordering = ['-executed_at']
