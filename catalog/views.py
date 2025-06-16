# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategoryWithSubSerializer, ProductFlatSerializer


class CatalogFlatView(APIView):
    def get(self, request):
        categories = Category.objects.prefetch_related('subcategories')
        products = Product.objects.prefetch_related('reasons', 'offer', 'subcategory')

        categories_data = CategoryWithSubSerializer(categories, many=True).data
        products_data = ProductFlatSerializer(products, many=True).data

        return Response({
            "categories": categories_data,
            "products": products_data
        })
