from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import random
from datetime import timedelta
from django.utils import timezone

class OTPRequest(models.Model):
    phone = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        return str(random.randint(10000, 99999))

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.name or 'Unverified'}"
