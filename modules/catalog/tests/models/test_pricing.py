from django.test import TestCase

from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Pricing,
    Product,
    ProductType,
    SellingCase,
    GradeConfiguration,
)
from modules.merchants.models import Merchant

from django.core.exceptions import ValidationError
from django.db import IntegrityError

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

        self.product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        self.grade_configuration = GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

    def test_fixed_pricing_can_be_created_for_merchant_selling_case(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=5000,
        )

        self.assertEqual(
            pricing.merchant_selling_case,
            self.merchant_selling_case,
        )
        self.assertEqual(pricing.behavior, Pricing.FIXED)
        self.assertEqual(pricing.amount, 5000)

    def test_fixed_pricing_requires_amount(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_fixed_pricing_cannot_have_rate(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=5000,
            rate=300,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_per_volume_pricing_can_be_created_for_merchant_selling_case(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=300,
        )

        self.assertEqual(
            pricing.merchant_selling_case,
            self.merchant_selling_case,
        )
        self.assertEqual(pricing.behavior, Pricing.PER_VOLUME)
        self.assertEqual(pricing.rate, 300)

    def test_per_volume_pricing_requires_rate(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_per_volume_pricing_cannot_have_amount(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=300,
            amount=5000,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_fixed_pricing_calculates_price(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=5000,
        )

        self.assertEqual(pricing.calculate_price(), 5000)

    def test_per_volume_pricing_calculates_price(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=300,
        )

        self.assertEqual(
            pricing.calculate_price(volume_ml=10),
            3000,
        )


    def test_per_volume_pricing_requires_volume_for_calculation(self):
        pricing = Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=300,
        )

        with self.assertRaises(ValidationError):
            pricing.calculate_price()


    def test_pricing_amount_cannot_be_negative(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=-100,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()


    def test_pricing_rate_cannot_be_negative(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=-100,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()


    def test_merchant_selling_case_can_have_only_one_pricing(self):
        Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=5000,
        )

        with self.assertRaises(IntegrityError):
            Pricing.objects.create(
                merchant_selling_case=self.merchant_selling_case,
                behavior=Pricing.FIXED,
                amount=6000,
            )

    def test_fixed_pricing_can_be_created_for_grade_configuration(self):
        pricing = Pricing.objects.create(
            grade_configuration=self.grade_configuration,
            behavior=Pricing.FIXED,
            amount=5000,
        )

        self.assertEqual(
            pricing.grade_configuration,
            self.grade_configuration,
        )
        self.assertEqual(pricing.behavior, Pricing.FIXED)
        self.assertEqual(pricing.amount, 5000)

    def test_pricing_cannot_belong_to_both_owners(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            grade_configuration=self.grade_configuration,
            behavior=Pricing.FIXED,
            amount=5000,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()


    def test_pricing_must_have_an_owner(self):
        pricing = Pricing(
            behavior=Pricing.FIXED,
            amount=5000,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_pricing_amount_cannot_be_zero(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount=0,
        )

        with self.assertRaises(ValidationError):
            pricing.full_clean()

    def test_pricing_rate_cannot_be_zero(self):
        pricing = Pricing(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.PER_VOLUME,
            rate=0,
        )
    
        with self.assertRaises(ValidationError):
            pricing.full_clean()