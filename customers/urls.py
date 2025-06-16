from django.urls import path
from .views import SendOTPView, VerifyOTPView, CustomerProfileView, UpdateLocationView, UpdateProfileView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('update-location/', UpdateLocationView.as_view(), name='update-location'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
]
