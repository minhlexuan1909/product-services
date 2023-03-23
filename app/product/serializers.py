"""
Serializes for product API
"""

from rest_framework import serializers

from .models import Product

from tag.serializers import TagSerializer
from tag.models import Tag


class ProductSerializer(serializers.ModelSerializer):
    """Serializes a product object"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ("id", "title", "price", "link", "image", "tags")
        read_only_fields = ("id",)

    def _get_or_create_tags(self, tags, product):
        """Handle getting or creating tags"""
        # auth_user = self.context["request"].user
        for tag in tags:
            tab_obj, created = Tag.objects.get_or_create(
                # user=auth_user,
                **tag
            )
            product.tags.add(tab_obj)

    def create(self, validated_data):
        """Create a new tag"""
        tags = validated_data.pop("tags", [])
        product = Product.objects.create(**validated_data)
        # auth_user = self.context["request"].user
        self._get_or_create_tags(tags, product)
        return product

    def update(self, instance, validated_data):
        """Update product"""
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProductDetailSerializer(ProductSerializer):
    """Serializes a product detail"""

    class Meta(ProductSerializer.Meta):
        # More infos about a product (Add description)
        fields = ProductSerializer.Meta.fields + ("description",)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to products"""

    class Meta:
        model = Product
        fields = ("id", "image")
        read_only_fields = ("id",)
        extra_kwargs = {"image": {"required": True}}
