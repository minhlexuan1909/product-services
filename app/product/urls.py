"""
URL mappings for the product app
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, BookViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("books", BookViewSet)

app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
]
