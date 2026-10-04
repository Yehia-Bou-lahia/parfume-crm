from django.db import models

from .product_type import ProductType


class SellingCase(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="selling_cases",
    )
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_type", "name"],
                name="unique_selling_case_per_product_type",
            ),
        ]

    def __str__(self):
        return self.name