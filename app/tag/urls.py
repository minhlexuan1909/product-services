"""
URL mappings for the tag app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()
router.register("tags", TagViewSet)

app_name = "tag"

urlpatterns = [
    path("", include(router.urls)),
]
