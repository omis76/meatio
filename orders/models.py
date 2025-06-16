from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta, date

User = get_user_model()

class OrderType(models.TextChoices):
    ONE_TIME = "one_time", "One Time"
    SUBSCRIPTION = "subscription", "Subscription"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.SUBSCRIPTION)
    start_date = models.DateField()
    end_date = models.DateField()
    days_of_week = models.JSONField(blank=True, null=True)  # e.g., ["mon", "wed"]
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} ({self.start_date} → {self.end_date})"

class Delivery(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.delivery_date}"

class DeliveryOverride(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date = models.DateField()
    new_quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('subscription', 'date')

    def __str__(self):
        return f"Override for {self.subscription} on {self.date}: {self.new_quantity}"

@receiver([post_save, post_delete], sender=Subscription)
def regenerate_deliveries(sender, instance, **kwargs):
    Delivery.objects.filter(subscription=instance, delivery_date__gte=date.today()).delete()

    if not instance.is_active:
        return

    current = max(date.today(), instance.start_date)
    end = instance.end_date

    while current <= end:
        weekday = current.strftime("%a").lower()
        if instance.order_type == OrderType.ONE_TIME:
            if current == instance.start_date:
                override = DeliveryOverride.objects.filter(subscription=instance, date=current).first()
                quantity = override.new_quantity if override else instance.quantity
                Delivery.objects.create(
                    subscription=instance,
                    user=instance.user,
                    product=instance.product,
                    quantity=quantity,
                    delivery_date=current
                )
        elif instance.order_type == OrderType.SUBSCRIPTION:
            if instance.days_of_week and weekday in instance.days_of_week:
                override = DeliveryOverride.objects.filter(subscription=instance, date=current).first()
                quantity = override.new_quantity if override else instance.quantity
                Delivery.objects.create(
                    subscription=instance,
                    user=instance.user,
                    product=instance.product,
                    quantity=quantity,
                    delivery_date=current
                )
        current += timedelta(days=1)