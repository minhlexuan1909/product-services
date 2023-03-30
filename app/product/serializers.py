"""
Serializes for product API
"""

from rest_framework import serializers

from .models import Product, Book, Clothes

from tag.serializers import TagSerializer
from tag.models import Tag


class ProductSerializer(serializers.ModelSerializer):
    """Serializes a product object"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "link",
            "image",
            "quantity",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def _get_or_create_tags(self, tags, product):
        """Handle getting or creating tags"""
        # auth_user = self.context["request"].user
        print("tags", tags)
        for tag in tags:
            tab_obj, created = Tag.objects.get_or_create(
                # user=auth_user,
                **tag
            )
            product.tags.add(tab_obj)

    def create(self, validated_data):
        """Create a new tag"""
        print("validated_data", validated_data)
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


class BookDetailSerializer(ProductDetailSerializer):
    """Serializes a book detail"""

    class Meta(ProductSerializer.Meta):
        model = Book
        # More infos about a book (Add author)
        fields = ProductSerializer.Meta.fields + ("author",)

    def create(self, validated_data):
        """Create a new tag"""
        print("validated_data", validated_data)
        tags = validated_data.pop("tags", [])
        book = Book.objects.create(**validated_data)
        # auth_user = self.context["request"].user
        self._get_or_create_tags(tags, book)
        return book


class ClothesDetailSerializer(ProductDetailSerializer):
    """Serializes a clothes detail"""

    class Meta(ProductSerializer.Meta):
        model = Clothes
        # More infos about a clothes (Add size)
        fields = ProductSerializer.Meta.fields + ("size",)

    def create(self, validated_data):
        """Create a new tag"""
        print("validated_data", validated_data)
        tags = validated_data.pop("tags", [])
        clothes = Clothes.objects.create(**validated_data)
        # auth_user = self.context["request"].user
        self._get_or_create_tags(tags, clothes)
        return clothes
