from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from customers.models import Customer
from dashboard.models import HomeBanner, HomeItem
from dashboard.serializers import HomeBannerSerializer, HomeItemSerializer
from wallet.models import Wallet
from catalog.models import Category
from catalog.serializers import SubcategoryFlatSerializer


class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer
        wallet, _ = Wallet.objects.get_or_create(customer=customer)

        address_line1 = customer.address_line1 or ""
        address_line2 = customer.address_line2 or ""
        full_address = f"{address_line1}, {address_line2}".strip(", ")

        category_data = []
        for category in Category.objects.all():
            subcategories = category.subcategories.all()
            sub_serializer = SubcategoryFlatSerializer(subcategories, many=True)
            category_data.append({
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "subcategories": sub_serializer.data
            })

        return Response({
            "address_line1": address_line1,
            "address_full": full_address,
            "wallet_balance": str(wallet.balance),  # or use float(wallet.balance)
            "categories": category_data
        })


class HomeScreenView(APIView):
    def get(self, request):
        banners = HomeBanner.objects.all()
        home_items = HomeItem.objects.prefetch_related('sub_items').all()

        banner_data = HomeBannerSerializer(banners, many=True).data
        item_data = HomeItemSerializer(home_items, many=True).data

        return Response({
            "banners": banner_data,
            "items": item_data
        })
