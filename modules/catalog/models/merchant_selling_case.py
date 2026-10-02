from django.core.exceptions import ValidationError
from django.db import models

from .merchant_product_type import MerchantProductType
from .selling_case import SellingCase


class MerchantSellingCase(models.Model):
    merchant_product_type = models.ForeignKey(
        MerchantProductType,
        on_delete=models.CASCADE,
        related_name="selling_case_configurations",
    )

    selling_case = models.ForeignKey(
        SellingCase,
        on_delete=models.CASCADE,
        related_name="merchant_configurations",
    )

    is_active = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if not self.merchant_product_type_id or not self.selling_case_id:
            return

        if (
            self.merchant_product_type.product_type_id
            != self.selling_case.product_type_id
        ):
            raise ValidationError(
                {
                    "selling_case": (
                        "Selling case must belong to the same product type "
                        "as the merchant product type."
                    )
                }
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant_product_type", "selling_case"],
                name="unique_merchant_selling_case",
            ),
        ]
