from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Pricing,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


class PricingTests(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.oil_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.oil_type,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=1,
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

    def test_merchant_can_configure_fixed_pricing(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.FIXED,
            amount=2500,
        )

        pricing.full_clean()
        pricing.save()

        self.assertEqual(
            pricing.merchant_selling_case,
            self.merchant_selling_case,
        )
        self.assertEqual(pricing.pricing_type, Pricing.FIXED)
        self.assertEqual(pricing.amount, 2500)

    def test_merchant_can_configure_per_volume_pricing(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.PER_VOLUME,
            rate=50,
        )

        pricing.full_clean()
        pricing.save()

        self.assertEqual(pricing.pricing_type, Pricing.PER_VOLUME)
        self.assertEqual(pricing.rate, 50)

    def test_merchant_selling_case_can_have_only_one_pricing(self):
        Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.FIXED,
            amount=2500,
        )

        with self.assertRaises(IntegrityError):
            Pricing.objects.create(
                merchant_selling_case=self.merchant_selling_case,
                pricing_type=Pricing.PER_VOLUME,
                rate=50,
            )

    def test_fixed_pricing_cannot_have_rate(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.FIXED,
            amount=2500,
            rate=50,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_per_volume_pricing_cannot_have_amount(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.PER_VOLUME,
            amount=2500,
            rate=50,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_fixed_pricing_calculates_price(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.FIXED,
            amount=2500,
        )

        self.assertEqual(
            pricing.calculate_price(),
            Decimal("2500.00"),
        )

    def test_per_volume_pricing_calculates_price(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            pricing_type=Pricing.PER_VOLUME,
            rate=50,
        )

        self.assertEqual(
            pricing.calculate_price(30),
            Decimal("1500.00"),
        )