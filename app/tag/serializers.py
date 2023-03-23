"""
Serializes for tag API
"""

from rest_framework import serializers

from .models import Tag
from product.models import Product


class TagSerializer(serializers.ModelSerializer):
    """Serializes a tag object"""

    class Meta:
        model = Tag
        fields = ("id", "name", "description")
        read_only_fields = ("id",)
