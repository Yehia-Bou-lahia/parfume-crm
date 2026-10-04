from decimal import Decimal

from rest_framework import serializers

from modules.catalog.models import (
    Product,
    ProductType,
    SellingCase,
)
from modules.catalog.models.grade_configuration import GradeConfiguration
from modules.catalog.models.merchant_product import MerchantProduct
from modules.catalog.models.merchant_product_type import MerchantProductType
from modules.catalog.models.merchant_selling_case import MerchantSellingCase
from modules.catalog.models.pricing import Pricing

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
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class ConfigureMerchantProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)


class MerchantProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True,
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = MerchantProduct
        fields = [
            "id",
            "product_id",
            "product_name",
            "is_active",
        ]
        read_only_fields = fields


class ConfigureMerchantProductTypeSerializer(serializers.Serializer):
    product_type_id = serializers.IntegerField(min_value=1)


class ConfigureMerchantSellingCaseSerializer(serializers.Serializer):
    selling_case_id = serializers.IntegerField(min_value=1)


class MerchantProductTypeSerializer(serializers.ModelSerializer):
    product_type_id = serializers.IntegerField(
        source="product_type.id",
        read_only=True,
    )
    product_type_name = serializers.CharField(
        source="product_type.name",
        read_only=True,
    )

    class Meta:
        model = MerchantProductType
        fields = [
            "id",
            "product_type_id",
            "product_type_name",
            "is_active",
        ]
        read_only_fields = fields


class MerchantSellingCaseSerializer(serializers.ModelSerializer):
    selling_case_id = serializers.IntegerField(
        source="selling_case.id",
        read_only=True,
    )

    selling_case_name = serializers.CharField(
        source="selling_case.name",
        read_only=True,
    )

    class Meta:
        model = MerchantSellingCase
        fields = [
            "id",
            "selling_case_id",
            "selling_case_name",
            "is_active",
        ]
        read_only_fields = fields


class ConfigureGradeConfigurationSerializer(serializers.Serializer):
    grade = serializers.IntegerField(min_value=1)


class GradeConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeConfiguration
        fields = [
            "id",
            "grade",
        ]
        read_only_fields = fields


class ConfigureMerchantSellingCasePricingSerializer(serializers.Serializer):
    behavior = serializers.ChoiceField(
        choices=Pricing.BEHAVIOR_CHOICES,
    )

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        required=False,
        allow_null=True,
    )

    rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        behavior = attrs["behavior"]
        amount = attrs.get("amount")
        rate = attrs.get("rate")

        if behavior == Pricing.FIXED:
            if amount is None:
                raise serializers.ValidationError(
                    {"amount": "Fixed pricing requires an amount."}
                )

            if rate is not None:
                raise serializers.ValidationError(
                    {"rate": "Fixed pricing cannot have a rate."}
                )

        elif behavior == Pricing.PER_VOLUME:
            if rate is None:
                raise serializers.ValidationError(
                    {"rate": "Per-volume pricing requires a rate."}
                )

            if amount is not None:
                raise serializers.ValidationError(
                    {"amount": "Per-volume pricing cannot have an amount."}
                )

        return attrs


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = [
            "id",
            "behavior",
            "amount",
            "rate",
        ]
        read_only_fields = fields