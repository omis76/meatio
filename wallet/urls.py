from django.urls import path
from .views import WalletView, WalletTransactionHistoryView, SuggestedAmountsView, RechargeWalletView, DebitWalletView

urlpatterns = [
    path('', WalletView.as_view()),
    path('history/', WalletTransactionHistoryView.as_view()),
    path('suggestions/', SuggestedAmountsView.as_view()),
    path('recharge/', RechargeWalletView.as_view()),
    path('debit/', DebitWalletView.as_view()),
]
