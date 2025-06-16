from rest_framework import serializers
from .models import HomeBanner, HomeItem, HomeSubItem
from catalog.models import Product, Subcategory
from catalog.serializers import ProductFlatSerializer, SubcategoryFlatSerializer


class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBanner
        fields = ['title', 'subtitle', 'image_url']


class GenericCardSerializer(serializers.Serializer):
    title = serializers.CharField()
    image_url = serializers.URLField()


class HomeSubItemSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        if obj.type == 'PRODUCT' and obj.product:
            return {
                "product": ProductFlatSerializer(obj.product).data
            }
        elif obj.type == 'SUBCATEGORY' and obj.subcategory:
            return {
                "subcategory": SubcategoryFlatSerializer(obj.subcategory).data
            }
        elif obj.type == 'GENERIC':
            return {
                "generic": {
                    "title": obj.generic_text,
                    "image_url": obj.generic_image_url
                }
            }
        return {}


class HomeItemSerializer(serializers.ModelSerializer):
    layoutType = serializers.CharField(source='layout_type')
    items = serializers.SerializerMethodField()
    title = serializers.CharField()
    subtitle = serializers.CharField()

    class Meta:
        model = HomeItem
        fields = ['title', 'subtitle', 'layoutType', 'items']

    def get_items(self, obj):
        sub_items = obj.sub_items.all()
        return HomeSubItemSerializer(sub_items, many=True).data
