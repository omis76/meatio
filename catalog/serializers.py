# serializers.py

from rest_framework import serializers
from .models import Category, Subcategory, Product, Reason, Offer


class SubcategoryFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'description', 'image']


class CategoryWithSubSerializer(serializers.ModelSerializer):
    subcategories = SubcategoryFlatSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'subcategories']


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['reason_text', 'reason_image']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'offer_text', 'offer_percentage', 'offer_price']


class ProductFlatSerializer(serializers.ModelSerializer):
    subcategoryId = serializers.IntegerField(source='subcategory.id')
    unitSize = serializers.CharField(source='unit_size')
    unitType = serializers.CharField(source='unit_type')
    unitText = serializers.CharField(source='unit_text')
    sellingPrice = serializers.CharField(source='selling_price')
    offerPrice = serializers.CharField(source='offer_price')
    deliveryText = serializers.CharField(source='delivery_text')
    reasons = ReasonSerializer(many=True)
    offer = OfferSerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'subcategoryId', 'image', 'name', 'unitSize', 'unitType',
            'unitText', 'mrp', 'sellingPrice', 'offerPrice', 'deliveryText',
            'description', 'reasons', 'offer'
        ]
