from django.urls import path
from .views import UserDashboardView, HomeScreenView

urlpatterns = [
    path('user-dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('home/', HomeScreenView.as_view(), name='home-screen'),
]
