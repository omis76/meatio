# urls.py
from django.urls import path
from .views import CatalogFlatView

urlpatterns = [
    path('', CatalogFlatView.as_view(), name='catalog-flat'),
]