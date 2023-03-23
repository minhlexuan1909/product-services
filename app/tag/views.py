from django.shortcuts import render

# Create your views here.
from django.core import serializers
from django.http import JsonResponse

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer
from product.serializers import ProductSerializer
from product.models import Product


class TagViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Manage tags in the database"""

    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        """List all tags"""
        # print(kwargs)
        tag = self.queryset.filter(id=kwargs["pk"])[0]
        product_in_tag = list(tag.product_set.all().values())
        tag_value = self.queryset.filter(id=kwargs["pk"]).values()[0]
        tag_value["products"] = product_in_tag

        # tag["products"] = list(product_in_tag)
        return Response(tag_value)
