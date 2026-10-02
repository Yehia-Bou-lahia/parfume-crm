from django.db import models

from .product import Product


class ProductType(models.Model):
    ORIGINAL = "ORIGINAL"
    OIL = "OIL"
    COMMERCIAL = "COMMERCIAL"
    STANDARD = "STANDARD"

    TYPE_CHOICES = [
        (ORIGINAL, "Original"),
        (OIL, "Oil"),
        (COMMERCIAL, "Commercial"),
        (STANDARD, "Standard"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_types",
    )

    name = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "name"],
                name="unique_product_type",
            ),
        ]
