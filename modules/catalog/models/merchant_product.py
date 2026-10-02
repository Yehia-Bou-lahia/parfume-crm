from django.db import models

from .product import Product


class MerchantProduct(models.Model):
    merchant = models.ForeignKey(
        "merchants.Merchant",
        on_delete=models.CASCADE,
        related_name="products",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="merchant_products",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "product"],
                name="unique_merchant_product",
            ),
        ]
