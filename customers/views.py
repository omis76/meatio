from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .models import Customer, OTPRequest
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import SendOTPSerializer, VerifyOTPSerializer, CustomerProfileSerializer


# --- Send OTP ---
class SendOTPView(APIView):
    permission_classes = [AllowAny]  # 👈 This line allows public access

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = OTPRequest.generate_otp()
            OTPRequest.objects.create(phone=phone, otp_code=otp)
            print(f"[DEBUG] OTP for {phone}: {otp}")  # Simulate SMS
            return Response({'message': 'OTP sent successfully (mocked)'})
        return Response(serializer.errors, status=400)


# --- Verify OTP ---
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]  # 👈 This line allows public access

    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        try:
            otp_entry = OTPRequest.objects.filter(phone=phone, is_verified=False).latest('created_at')
        except OTPRequest.DoesNotExist:
            return Response({'error': 'No OTP request found'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_entry.is_expired():
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_entry.otp_code != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        otp_entry.is_verified = True
        otp_entry.save()

        customer, _ = Customer.objects.get_or_create(phone=phone)
        customer.is_verified = True

        if not customer.user:
            User = get_user_model()
            user = User.objects.create_user(email=f"{phone}@meatio.fake", password=None)
            customer.user = user
            customer.save()
        else:
            user = customer.user

        # Create or return token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'OTP verified successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            data = {
                "phone": customer.phone,
                "name": customer.name,
                "address_line1": customer.address_line1,
                "address_line2": customer.address_line2,
                "latitude": customer.latitude,
                "longitude": customer.longitude,
                "created_at": customer.created_at
            }
            return Response(data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found"}, status=404)


class UpdateLocationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found"}, status=status.HTTP_404_NOT_FOUND)

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude is not None:
            customer.latitude = latitude
        if longitude is not None:
            customer.longitude = longitude

        customer.save()

        return Response({
            'message': 'Location updated successfully.',
            'latitude': customer.latitude,
            'longitude': customer.longitude
        }, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found"}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get("name")
        address_line1 = request.data.get("address_line1")
        address_line2 = request.data.get("address_line2")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if name:
            customer.name = name
        if address_line1:
            customer.address_line1 = address_line1
        if address_line2:
            customer.address_line2 = address_line2
        if latitude is not None:
            customer.latitude = latitude
        if longitude is not None:
            customer.longitude = longitude

        customer.save()

        return Response({
            'message': 'Profile updated successfully.',
            'name': customer.name,
            'address_line1': customer.address_line1,
            'address_line2': customer.address_line2,
            'latitude': customer.latitude,
            'longitude': customer.longitude
        }, status=status.HTTP_200_OK)
