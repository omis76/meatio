"""
URL configuration for meatio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Meatio API",
        default_version='v1',
        description="API documentation for Meatio project",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="support@meatio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customer/', include('customers.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/orders/', include('orders.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
