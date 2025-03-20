# apps/gamification/models.py
from django.db import models
from apps.authentication.models import User

class KenoEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=50)  # Comma-separated numbers
    entry_time = models.DateTimeField(auto_now_add=True)
