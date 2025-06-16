from django.db import models
from customers.models import Customer


class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)


class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('RECHARGE', 'Recharge'),
        ('DEBIT', 'Debit'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SuggestedAmount(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
