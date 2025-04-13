from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Asset(models.Model):
    ASSET_TYPES = (
        ('equity', 'Equity'),
        ('bond', 'Bond'),
        ('derivative', 'Derivative'),
        ('fx', 'Foreign Exchange'),
    )
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)

    def __str__(self):
        return f"{self.symbol} ({self.asset_type})"

class Order(models.Model):
    ORDER_TYPES = (
        ('market', 'Market'),
        ('limit', 'Limit'),
        ('stop', 'Stop'),
        ('fok', 'Fill or Kill'),
        ('ioc', 'Immediate or Cancel'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('filled', 'Filled'),
        ('partially_filled', 'Partially Filled'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    quantity = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.order_type} {self.asset} {self.quantity}"
