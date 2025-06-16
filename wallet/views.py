
from .serializers import WalletSerializer, WalletTransactionSerializer, SuggestedAmountSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, WalletTransaction, SuggestedAmount
from decimal import Decimal


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(customer=request.user.customer)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletTransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(customer=request.user.customer)
        transactions = wallet.transactions.order_by('-created_at')
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class SuggestedAmountsView(APIView):
    def get(self, request):
        amounts = SuggestedAmount.objects.all().order_by('amount')
        serializer = SuggestedAmountSerializer(amounts, many=True)
        return Response(serializer.data)


class RechargeWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")

            wallet, _ = Wallet.objects.get_or_create(customer=request.user.customer)
            wallet.balance += amount
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='RECHARGE',
                description="Wallet recharge"
            )

            return Response({"message": "Wallet recharged successfully", "new_balance": str(wallet.balance)})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DebitWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description', 'Order deduction')

        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")

            wallet = Wallet.objects.get(customer=request.user.customer)
            if wallet.balance < amount:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            wallet.balance -= amount
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='DEBIT',
                description=description
            )

            return Response({"message": "Amount debited successfully", "new_balance": str(wallet.balance)})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)