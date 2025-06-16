from django.contrib import admin
from .models import HomeBanner, HomeItem, HomeSubItem
from catalog.models import Product, Subcategory


# Admin for HomeBanner
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image_url')
    search_fields = ('title', 'subtitle')
    ordering = ('title',)


admin.site.register(HomeBanner, HomeBannerAdmin)


# Admin for HomeItem
class HomeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'layout_type')
    search_fields = ('title', 'subtitle')
    list_filter = ('layout_type',)
    filter_horizontal = ('banners',)  # This adds a widget to select HomeBanners for each HomeItem
    ordering = ('title',)


admin.site.register(HomeItem, HomeItemAdmin)


# Admin for HomeSubItem
class HomeSubItemAdmin(admin.ModelAdmin):
    list_display = ('type', 'home_item', 'product', 'subcategory', 'generic_text')
    search_fields = ('home_item__title', 'product__name', 'subcategory__name', 'generic_text')
    list_filter = ('type',)


admin.site.register(HomeSubItem, HomeSubItemAdmin)
