from django.contrib import admin
from .models import Category, Subcategory, Product, Offer, Reason


class ReasonInline(admin.TabularInline):
    model = Reason
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'mrp', 'selling_price', 'offer_price', 'unit_size', 'unit_type')
    search_fields = ('name', 'subcategory__name')
    list_filter = ('subcategory',)
    inlines = [ReasonInline]


class OfferAdmin(admin.ModelAdmin):
    list_display = ('offer_text', 'offer_percentage', 'offer_price')
    search_fields = ('offer_text',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


# Register the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Reason)