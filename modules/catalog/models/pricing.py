
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .merchant_selling_case import MerchantSellingCase
from .grade_configuration import GradeConfiguration


class Pricing(models.Model):
    FIXED = "FIXED"
    PER_VOLUME = "PER_VOLUME"

    BEHAVIOR_CHOICES = [
        (FIXED, "Fixed"),
        (PER_VOLUME, "Per Volume"),
    ]

    merchant_selling_case = models.OneToOneField(
        MerchantSellingCase,
        on_delete=models.CASCADE,
        related_name="pricing",
        null=True,
        blank=True,
    )

    grade_configuration = models.OneToOneField(
        GradeConfiguration,
        on_delete=models.CASCADE,
        related_name="pricing",
        null=True,
        blank=True,
    )

    behavior = models.CharField(
        max_length=20,
        choices=BEHAVIOR_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def clean(self):
        super().clean()

        has_merchant_selling_case = (
            self.merchant_selling_case_id is not None
        )
        has_grade_configuration = (
            self.grade_configuration_id is not None
        )

        if has_merchant_selling_case == has_grade_configuration:
            raise ValidationError(
                "Pricing must belong to exactly one owner."
            )

        if self.behavior == self.FIXED:
            if self.amount is None:
                raise ValidationError(
                    {"amount": "Fixed pricing requires an amount."}
                )

            if self.rate is not None:
                raise ValidationError(
                    {"rate": "Fixed pricing cannot have a rate."}
                )

        elif self.behavior == self.PER_VOLUME:
            if self.rate is None:
                raise ValidationError(
                    {"rate": "Per-volume pricing requires a rate."}
                )

            if self.amount is not None:
                raise ValidationError(
                    {"amount": "Per-volume pricing cannot have an amount."}
                )

    def calculate_price(self, volume_ml=None):
        if self.behavior == self.FIXED:
            return self.amount

        if self.behavior == self.PER_VOLUME:
            if volume_ml is None:
                raise ValidationError(
                    {"volume_ml": "Volume is required for per-volume pricing."}
                )

            volume_ml = Decimal(str(volume_ml))
            return self.rate * volume_ml

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__isnull=True) | Q(amount__gt=0),
                name="pricing_amount_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(rate__isnull=True) | Q(rate__gt=0),
                name="pricing_rate_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        merchant_selling_case__isnull=False,
                        grade_configuration__isnull=True,
                    )
                    | Q(
                        merchant_selling_case__isnull=True,
                        grade_configuration__isnull=False,
                    )
                ),
                name="pricing_exactly_one_owner",
            ),
        ]