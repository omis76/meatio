from django.contrib import admin
from .models import PaymentType, PaymentMethod, Payment


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('method', 'name', 'payment_type')
    list_filter = ('payment_type',)
    search_fields = ('method', 'name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'customer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'customer__phone', 'customer__user__email')
    readonly_fields = ('created_at', 'payment_id')
