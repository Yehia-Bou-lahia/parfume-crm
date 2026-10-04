from django.core.validators import MinValueValidator
from django.db import models

from .merchant_selling_case import MerchantSellingCase


class GradeConfiguration(models.Model):
    merchant_selling_case = models.ForeignKey(
        MerchantSellingCase,
        on_delete=models.CASCADE,
        related_name="grade_configurations",
    )

    grade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant_selling_case", "grade"],
                name="unique_grade_per_merchant_selling_case",
            ),
        ]