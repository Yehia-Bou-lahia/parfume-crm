from rest_framework import serializers

from modules.catalog.models import Product, ProductType, SellingCase


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = [
            "id",
            "product",
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class SellingCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellingCase
        fields = [
            "id",
            "product_type",
            "volume_ml",
        ]
        read_only_fields = [
            "id",
        ]