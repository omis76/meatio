from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .models import Subscription, Delivery, DeliveryOverride
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['product', 'order_type', 'is_active']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    search_fields = ['product__name']

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyDeliveriesByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.GET.get('date')
        if not date_str:
            return Response({"error": "date query param is required (YYYY-MM-DD)"}, status=400)

        try:
            delivery_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            deliveries = Delivery.objects.filter(user=request.user, delivery_date=delivery_date)
            data = [
                {
                    "subscription": d.subscription.id,
                    "product": d.product.id,
                    "quantity": d.quantity,
                    "status": d.status,
                    "delivery_date": d.delivery_date
                }
                for d in deliveries
            ]
            return Response(data)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)


class UpdateDeliveryOverridesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = request.data
        if not isinstance(payload, list):
            return Response({"error": "Expected a list of overrides."}, status=400)

        created = 0
        updated = 0

        for item in payload:
            try:
                subscription = Subscription.objects.get(id=item['subscription'], user=request.user)
                date = datetime.strptime(item['date'], "%Y-%m-%d").date()
                new_quantity = int(item['new_quantity'])

                obj, was_created = DeliveryOverride.objects.update_or_create(
                    subscription=subscription,
                    date=date,
                    defaults={"new_quantity": new_quantity}
                )

                if was_created:
                    created += 1
                else:
                    updated += 1

                # update delivery row if it exists
                Delivery.objects.filter(subscription=subscription, delivery_date=date).update(quantity=new_quantity)

            except (Subscription.DoesNotExist, KeyError, ValueError):
                continue

        return Response({"created": created, "updated": updated})

