from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class MerchantProductType(models.Model):
    merchant_product = models.ForeignKey(
        MerchantProduct,
        on_delete=models.CASCADE,
        related_name="product_type_configurations",
    )

    product_type = models.ForeignKey(
        "ProductType",
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