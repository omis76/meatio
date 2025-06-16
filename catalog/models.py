from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)  # Or use ImageField if needed

    def __str__(self):
        return f"{self.category.name} > {self.name}"


class Offer(models.Model):
    offer_text = models.CharField(max_length=255)
    offer_percentage = models.FloatField()
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.offer_text


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    image = models.URLField(blank=True)
    name = models.CharField(max_length=255)
    unit_size = models.CharField(max_length=50)        # e.g. '500g', '1L'
    unit_type = models.CharField(max_length=50)        # e.g. 'kg', 'ltr'
    unit_text = models.CharField(max_length=100, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_text = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Reason(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reasons')
    reason_text = models.CharField(max_length=255)
    reason_image = models.URLField(blank=True)

    def __str__(self):
        return f"{self.product.name}: {self.reason_text}"