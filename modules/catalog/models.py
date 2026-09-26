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
    default_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    
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
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "product_type"],
                name="unique_merchant_product_type",
            ),
        ]