# models/option.py
from django.db import models
from django.contrib.auth.models import User

class OptionContract(models.Model):
    SYMBOL_TYPE = [("CALL", "Call"), ("PUT", "Put")]

    underlying_asset = models.CharField(max_length=20)
    symbol = models.CharField(max_length=50, unique=True)
    option_type = models.CharField(choices=SYMBOL_TYPE, max_length=4)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    contract_size = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.symbol} ({self.option_type})"

class OptionTrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(OptionContract, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, choices=[("BUY", "Buy"), ("SELL", "Sell")])
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
