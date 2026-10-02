from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .merchant_selling_case import MerchantSellingCase


class Pricing(models.Model):
    FIXED = "FIXED"
    PER_VOLUME = "PER_VOLUME"

    PRICING_TYPE_CHOICES = [
        (FIXED, "Fixed"),
        (PER_VOLUME, "Per Volume"),
    ]

    merchant_selling_case = models.OneToOneField(
        MerchantSellingCase,
        on_delete=models.CASCADE,
        related_name="pricing",
    )

    pricing_type = models.CharField(
        max_length=20,
        choices=PRICING_TYPE_CHOICES,
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

        if self.pricing_type == self.FIXED:
            if self.amount is None:
                raise ValidationError(
                    {"amount": "Fixed pricing requires an amount."}
                )

            if self.rate is not None:
                raise ValidationError(
                    {"rate": "Fixed pricing cannot have a rate."}
                )

        elif self.pricing_type == self.PER_VOLUME:
            if self.rate is None:
                raise ValidationError(
                    {"rate": "Per-volume pricing requires a rate."}
                )

            if self.amount is not None:
                raise ValidationError(
                    {"amount": "Per-volume pricing cannot have an amount."}
                )

    def calculate_price(self, volume_ml=None):
        if self.pricing_type == self.FIXED:
            return self.amount

        if self.pricing_type == self.PER_VOLUME:
            if volume_ml is None:
                raise ValidationError(
                    {"volume_ml": "Volume is required for per-volume pricing."}
                )

            volume_ml = Decimal(str(volume_ml))
            return self.rate * volume_ml

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__isnull=True) | Q(amount__gte=0),
                name="pricing_amount_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(rate__isnull=True) | Q(rate__gte=0),
                name="pricing_rate_non_negative",
            ),
        ]
