from django.core.exceptions import ValidationError
from django.db import models

from modules.merchants.models import Merchant


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductType(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_types",
    )
    name = models.CharField(max_length=100)


class SellingCase(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="selling_cases",
    )
    volume_ml = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self):
        super().clean()

        if self.product_type_id and self.product_type.merchant_configurations.exists():
            raise ValidationError(
                "A product type with merchant configurations "
                "cannot have selling cases."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_type", "volume_ml"],
                name="unique_product_type_volume",
            ),
        ]


class MerchantProductConfiguration(models.Model):
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="product_configurations",
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="merchant_configurations",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if self.product_type_id and self.product_type.selling_cases.exists():
            raise ValidationError(
                "A product type with selling cases cannot use "
                "MerchantProductConfiguration."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "product_type"],
                name="unique_merchant_product_type",
            ),
        ]


class MerchantSellingCase(models.Model):
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="selling_case_configurations",
    )
    selling_case = models.ForeignKey(
        SellingCase,
        on_delete=models.CASCADE,
        related_name="merchant_configurations",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if self.selling_case_id and self.merchant_id:
            product_type = self.selling_case.product_type

            if MerchantProductConfiguration.objects.filter(
                merchant=self.merchant,
                product_type=product_type,
            ).exists():
                raise ValidationError(
                    "A merchant cannot configure a selling case "
                    "when the product type is already configured."
                )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "selling_case"],
                name="unique_merchant_selling_case",
            ),
        ]
