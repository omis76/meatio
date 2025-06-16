from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from datetime import datetime, date

from common.admin_filters import default_date_filter_gen
from . import models
from .models import Subscription, OrderType, Delivery


class WeekdayFilter(admin.SimpleListFilter):
    title = 'Day of Week'
    parameter_name = 'day_of_week'

    def lookups(self, request, model_admin):
        return [
            ('mon', 'Monday'),
            ('tue', 'Tuesday'),
            ('wed', 'Wednesday'),
            ('thu', 'Thursday'),
            ('fri', 'Friday'),
            ('sat', 'Saturday'),
            ('sun', 'Sunday'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(days_of_week__contains=[self.value()])
        return queryset


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'delivery_date', 'status']
    list_filter = ['status', 'delivery_date', 'product', 'user', default_date_filter_gen()]
    search_fields = ['user__username', 'product__name']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'order_type', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'order_type', 'product', 'user', WeekdayFilter]
    search_fields = ['user__username', 'product__name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('scheduled-orders/', self.admin_site.admin_view(self.orders_by_date_view), name='scheduled-orders'),
        ]
        return custom_urls + urls

    def orders_by_date_view(self, request):
        date_str = request.GET.get("date")
        subscriptions = []
        if date_str:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            weekday = selected_date.strftime("%a").lower()

            subscriptions = Subscription.objects.filter(
                is_active=True,
                start_date__lte=selected_date,
                end_date__gte=selected_date
            ).filter(
                models.Q(order_type=OrderType.ONE_TIME, start_date=selected_date) |
                models.Q(order_type=OrderType.SUBSCRIPTION, days_of_week__contains=[weekday])
            )

        context = dict(
            self.admin_site.each_context(request),
            title="Orders Scheduled on a Date",
            subscriptions=subscriptions,
            selected_date=date_str,
        )
        return render(request, "admin/orders/scheduled_orders.html", context)
