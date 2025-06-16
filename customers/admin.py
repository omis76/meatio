from django.contrib import admin
from .models import Customer, OTPRequest
from django.utils.html import format_html


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'is_verified', 'latitude', 'longitude', 'map_preview')
    readonly_fields = ('map_preview', 'created_at')
    search_fields = ('phone', 'name')
    list_filter = ('is_verified',)

    def map_preview(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<iframe width="300" height="200" frameborder="0" style="border:0" '
                'src="https://maps.google.com/maps?q={},{}&hl=es&z=14&output=embed" '
                'allowfullscreen></iframe>',
                obj.latitude, obj.longitude
            )
        return "No location set"

    map_preview.short_description = "Location on Map"


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp_code', 'is_verified', 'created_at')
    search_fields = ('phone',)
    list_filter = ('is_verified', 'created_at')
    readonly_fields = ('otp_code', 'created_at')
