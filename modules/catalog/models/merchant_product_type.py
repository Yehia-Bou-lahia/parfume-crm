from django.db import models

from .merchant_product import MerchantProduct
from .product_type import ProductType


class MerchantProductType(models.Model):
    merchant_product = models.ForeignKey(
        MerchantProduct,
        on_delete=models.CASCADE,
        related_name="product_type_configurations",
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
                fields=["merchant_product", "product_type"],
                name="unique_merchant_product_type",
            ),
        ]
