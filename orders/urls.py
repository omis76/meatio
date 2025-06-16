from django.urls import path
from .views import SubscriptionViewSet, MyDeliveriesByDateView, UpdateDeliveryOverridesView

subscription_list = SubscriptionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

subscription_detail = SubscriptionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('subscriptions/', subscription_list, name='subscription-list'),
    path('subscriptions/<int:pk>/', subscription_detail, name='subscription-detail'),
    path('my-deliveries/', MyDeliveriesByDateView.as_view(), name='my-deliveries'),
    path('updateDeliveries/', UpdateDeliveryOverridesView.as_view(), name='update-deliveries'),
]
