from rest_framework import serializers
from .models import Wallet, WalletTransaction, SuggestedAmount


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'updated_at']


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'


class SuggestedAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedAmount
        fields = ['amount']
