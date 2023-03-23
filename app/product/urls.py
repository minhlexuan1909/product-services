"""
URL mappings for the product app
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)

app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
]
