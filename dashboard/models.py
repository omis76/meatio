from django.db import models
from catalog.models import Category, Subcategory  # assuming you have a Category model
from catalog.models import Product  # assuming you have a Product model


class HomeBanner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image_url = models.URLField()

    def __str__(self):
        return self.title


class HomeItem(models.Model):
    LAYOUT_TYPE_CHOICES = [
        ('GRID', 'Grid'),
        ('HORIZONTAL', 'Horizontal'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    layout_type = models.CharField(max_length=10, choices=LAYOUT_TYPE_CHOICES)
    banners = models.ManyToManyField(HomeBanner, related_name='home_items', blank=True)

    def __str__(self):
        return self.title


class HomeSubItem(models.Model):
    TYPE_CHOICES = [
        ('PRODUCT', 'Product'),
        ('SUBCATEGORY', 'Subcategory'),
        ('GENERIC', 'Generic'),
    ]

    home_item = models.ForeignKey(HomeItem, on_delete=models.CASCADE, related_name='sub_items')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    generic_text = models.CharField(max_length=255, blank=True)
    generic_image_url = models.URLField(blank=True)

    def __str__(self):
        if self.type == 'PRODUCT':
            return f"Product: {self.product.name}"
        elif self.type == 'SUBCATEGORY':
            return f"Subcategory: {self.subcategory.name}"
        elif self.type == 'GENERIC':
            return f"Generic: {self.generic_text}"
        return "Unknown"


class GenericCard(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    text = models.TextField()

    def __str__(self):
        return self.title