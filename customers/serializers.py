from rest_framework import serializers
from .models import Customer

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'phone', 'name',
            'address_line1', 'address_line2',
            'latitude', 'longitude'
        ]