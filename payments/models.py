from django.db import models
from customers.models import Customer
import uuid


class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.URLField(blank=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='methods')
    method = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.URLField(blank=True)

    class Meta:
        unique_together = ('payment_type', 'method')

    def __str__(self):
        return f"{self.payment_type.name} - {self.name}"


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)
