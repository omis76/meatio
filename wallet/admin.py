# wallet/admin.py

from django.contrib import admin
from .models import Wallet, WalletTransaction, SuggestedAmount


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'balance', 'updated_at')
    search_fields = ('customer__phone', 'customer__user__email')
    readonly_fields = ('updated_at',)


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('wallet__customer__phone', 'wallet__customer__user__email')
    readonly_fields = ('created_at',)


@admin.register(SuggestedAmount)
class SuggestedAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount')
    ordering = ('amount',)
