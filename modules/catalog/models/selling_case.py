from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from .product_type import ProductType

class SellingCase(models.Model):
    QUALITY_LOW = "LOW"
    QUALITY_MEDIUM = "MEDIUM"
    QUALITY_HIGH = "HIGH"

    QUALITY_CHOICES = [
        (QUALITY_LOW, "Low"),
        (QUALITY_MEDIUM, "Medium"),
        (QUALITY_HIGH, "High"),
    ]

    AGED = "AGED"
    NON_AGED = "NON_AGED"

    AGING_CHOICES = [
        (AGED, "Aged"),
        (NON_AGED, "Non-aged"),
    ]

    FULL_BOTTLE = "FULL_BOTTLE"
    PORTION = "PORTION"

    SALE_MODE_CHOICES = [
        (FULL_BOTTLE, "Full Bottle"),
        (PORTION, "Portion"),
    ]

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="selling_cases",
    )

    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        null=True,
        blank=True,
    )

    aging = models.CharField(
        max_length=10,
        choices=AGING_CHOICES,
        null=True,
        blank=True,
    )

    grade = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    sale_mode = models.CharField(
        max_length=20,
        choices=SALE_MODE_CHOICES,
        null=True,
        blank=True,
    )

    def clean(self):
        super().clean()

        if not self.product_type_id:
            return

        validators = {
            ProductType.COMMERCIAL: self._validate_commercial,
            ProductType.OIL: self._validate_oil,
            ProductType.ORIGINAL: self._validate_original,
            ProductType.STANDARD: self._validate_standard,
        }

        validator = validators.get(self.product_type.name)

        if validator:
            validator()

    def _validate_commercial(self):
        if self.quality is None:
            raise ValidationError(
                {"quality": "Commercial selling cases require a quality."}
            )

        if self.aging is not None:
            raise ValidationError(
                {"aging": "Commercial selling cases cannot have aging."}
            )

        if self.grade is not None:
            raise ValidationError(
                {"grade": "Commercial selling cases cannot have a grade."}
            )

        if self.sale_mode is not None:
            raise ValidationError(
                {
                    "sale_mode": (
                        "Commercial selling cases cannot have a sale mode."
                    )
                }
            )

    def _validate_oil(self):
        if self.aging is None:
            raise ValidationError(
                {"aging": "Oil selling cases require aging."}
            )

        if self.grade is None:
            raise ValidationError(
                {"grade": "Oil selling cases require a grade."}
            )

        if self.grade <= 0:
            raise ValidationError(
                {"grade": "Grade must be greater than zero."}
            )

        if self.quality is not None:
            raise ValidationError(
                {"quality": "Oil selling cases cannot have a quality."}
            )

        if self.sale_mode is not None:
            raise ValidationError(
                {"sale_mode": "Oil selling cases cannot have a sale mode."}
            )

    def _validate_original(self):
        if self.sale_mode is None:
            raise ValidationError(
                {"sale_mode": "Original selling cases require a sale mode."}
            )

        if self.quality is not None:
            raise ValidationError(
                {"quality": "Original selling cases cannot have a quality."}
            )

        if self.aging is not None:
            raise ValidationError(
                {"aging": "Original selling cases cannot have aging."}
            )

        if self.grade is not None:
            raise ValidationError(
                {"grade": "Original selling cases cannot have a grade."}
            )

    def _validate_standard(self):
        if any(
            value is not None
            for value in (
                self.quality,
                self.aging,
                self.grade,
                self.sale_mode,
            )
        ):
            raise ValidationError(
                "Standard selling cases cannot have extra attributes."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product_type",
                    "quality",
                    "aging",
                    "grade",
                    "sale_mode",
                ],
                name="unique_selling_case",
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                condition=Q(grade__isnull=True) | Q(grade__gt=0),
                name="selling_case_grade_positive",
            ),
        ]
