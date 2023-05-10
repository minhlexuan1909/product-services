"""
Views for the product API
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Product, Book, Clothes
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    BookDetailSerializer,
    ClothesDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by name",
            ),
            OpenApiParameter(
                name="tags",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by tags (Comma seperated)",
            ),
            OpenApiParameter(
                name="idList",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by list of id (Comma seperated)",
            ),
        ],
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    """Manage products in the database"""

    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # return self.queryset.filter(user=self.request.user).order_by("-id")
        queryset = self.queryset
        name = self.request.query_params.get("name")
        tags = self.request.query_params.get("tags")
        idList = self.request.query_params.get("idList")
        if name:
            queryset = queryset.filter(title__icontains=name)
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if idList:
            idList_ids = self._params_to_ints(idList)
            queryset = queryset.filter(id__in=idList_ids)
        # return self.queryset.order_by("-id")
        return queryset.order_by("-id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "list":
            return ProductSerializer
        elif self.action == "upload_image":
            return ProductImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new product"""
        # Attach to user: serializer.save(user=self.request.user)
        serializer.save()

    # detail=True means that the view will be called on a single object,
    #  that means api goes with id like /product/{id}/upload-image
    # (False for a list of objects like /product/upload-image)
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to a product"""
        product = self.get_object()
        # Run get_serializer_class to get instance of serializer
        serializer = self.get_serializer(
            product,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(ProductViewSet):
    """Manage books in the database"""

    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "detail" or self.action == "list":
            return BookDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        print("serializer", serializer)
        """Create a new book"""
        # Attach to user: serializer.save(user=self.request.user)
        serializer.save()
        # return Response({})


class BookViewSet(ProductViewSet):
    """Manage books in the database"""

    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "detail" or self.action == "list":
            return BookDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        print("serializer", serializer)
        """Create a new book"""
        # Attach to user: serializer.save(user=self.request.user)
        serializer.save()
        # return Response({})


class ClothesViewSet(ProductViewSet):
    """Manage books in the database"""

    serializer_class = ClothesDetailSerializer
    queryset = Clothes.objects.all()
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "detail" or self.action == "list":
            return self.serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        print("serializer", serializer)
        """Create a new clothes"""
        # Attach to user: serializer.save(user=self.request.user)
        serializer.save()
        # return Response({})
