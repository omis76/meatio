from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Payment, PaymentType, PaymentStatus
from customers.models import Customer
from wallet.models import Wallet, WalletTransaction
from .serializers import PaymentTypeSerializer


class InitiatePaymentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        customer_id = request.data.get('customer_id')
        amount = request.data.get('amount')
        if not customer_id or not amount:
            return Response({'error': 'customer_id and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(id=customer_id)
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid customer'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.create(customer=customer, amount=amount)
        payment_types = PaymentType.objects.prefetch_related('methods').all()
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response({'payment_id': str(payment.payment_id), 'payment_types': serializer.data})


class PaymentStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            return Response({'payment_id': str(payment.payment_id), 'status': payment.status})
        except Payment.DoesNotExist:
            return Response({'error': 'Invalid payment id'}, status=status.HTTP_404_NOT_FOUND)


class UpdatePaymentStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, payment_id):
        status_value = request.data.get('status')
        if not status_value:
            return Response({'error': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Invalid payment id'}, status=status.HTTP_404_NOT_FOUND)
        payment.status = status_value
        payment.save()
        if status_value == PaymentStatus.SUCCESS:
            wallet, _ = Wallet.objects.get_or_create(customer=payment.customer)
            wallet.balance += payment.amount
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                amount=payment.amount,
                transaction_type='RECHARGE',
                description=f'Payment {payment.payment_id}'
            )
        return Response({'payment_id': str(payment.payment_id), 'status': payment.status})
