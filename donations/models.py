from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import uuid

class DonationCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Donation(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]

    CURRENCIES = [
        ('KES', 'Kenyan Shilling'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey(DonationCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='USD')  # Currency choices added
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    message = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())[:12]  # Auto-generate if missing
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name or 'Anonymous'} - {self.amount} {self.currency} via {self.payment_method}"
