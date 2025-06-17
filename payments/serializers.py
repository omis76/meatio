from rest_framework import serializers
from .models import PaymentType, PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['method', 'name', 'description', 'logo']


class PaymentTypeSerializer(serializers.ModelSerializer):
    methods = PaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'description', 'icon', 'methods']
