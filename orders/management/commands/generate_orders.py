from django.core.management.base import BaseCommand
from datetime import date
from orders.models import Subscription, OrderType


class Command(BaseCommand):
    help = 'Generate orders for today from subscriptions'

    def handle(self, *args, **kwargs):
        today = date.today()
        weekday = today.strftime("%a").lower()  # e.g., "mon"

        eligible = []

        subscriptions = Subscription.objects.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        )

        for sub in subscriptions:
            if sub.order_type == OrderType.ONE_TIME:
                if sub.start_date == today:
                    eligible.append(sub)
            elif sub.order_type == OrderType.SUBSCRIPTION:
                if sub.days_of_week and weekday in sub.days_of_week:
                    eligible.append(sub)

        for sub in eligible:
            self.stdout.write(f"[✔] Delivery: {sub.user} - {sub.product.name} - Qty: {sub.quantity} for {today}")

        self.stdout.write(self.style.SUCCESS(f"Generated {len(eligible)} deliveries"))
