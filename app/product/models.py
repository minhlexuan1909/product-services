from django.db import models
from tag.models import Tag

import uuid
import os


def product_image_file_path(instance, filename):
    """Generate file path for new product image"""
    # Extract file extension from filename (.png, .jpg, etc.)
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads", "product", filename)


class Product(models.Model):
    """Product object"""

    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, upload_to=product_image_file_path)
    quantity = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Book(Product):
    """Book object"""

    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title


SIZE = (
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
)


class Clothes(Product):
    """Clothes object"""

    size = models.CharField(max_length=255, choices=SIZE)

    def __str__(self):
        return self.title
