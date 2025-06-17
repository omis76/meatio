from django.urls import path
from .views import InitiatePaymentView, PaymentStatusView, UpdatePaymentStatusView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view()),
    path('<uuid:payment_id>/status/', PaymentStatusView.as_view()),
    path('<uuid:payment_id>/update/', UpdatePaymentStatusView.as_view()),
]
