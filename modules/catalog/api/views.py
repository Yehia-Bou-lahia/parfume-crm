from rest_framework import generics

from modules.catalog.api.serializers import (
    ProductSerializer,
    ProductTypeSerializer,
)
from modules.catalog.models import Product, ProductType


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductTypeListView(generics.ListAPIView):
    queryset = ProductType.objects.select_related("product")
    serializer_class = ProductTypeSerializer