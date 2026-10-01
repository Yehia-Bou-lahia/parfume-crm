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
from decimal import Decimal

class SellingCaseTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.oil_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.commercial_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.COMMERCIAL,
        )

        self.original_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.standard_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.STANDARD,
        )

    def test_oil_selling_case_stores_aging_and_grade(self):
        selling_case = SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        self.assertEqual(selling_case.product_type, self.oil_type)
        self.assertEqual(selling_case.aging, SellingCase.AGED)
        self.assertEqual(selling_case.grade, 2)

    def test_commercial_selling_case_stores_quality(self):
        selling_case = SellingCase.objects.create(
            product_type=self.commercial_type,
            quality=SellingCase.QUALITY_LOW,
        )

        self.assertEqual(selling_case.product_type, self.commercial_type)
        self.assertEqual(selling_case.quality, SellingCase.QUALITY_LOW)

    def test_original_selling_case_stores_sale_mode(self):
        selling_case = SellingCase.objects.create(
            product_type=self.original_type,
            sale_mode=SellingCase.FULL_BOTTLE,
        )

        self.assertEqual(selling_case.product_type, self.original_type)
        self.assertEqual(selling_case.sale_mode, SellingCase.FULL_BOTTLE)

    def test_standard_selling_case_has_no_extra_attributes(self):
        selling_case = SellingCase.objects.create(
            product_type=self.standard_type,
        )

        self.assertIsNone(selling_case.quality)
        self.assertIsNone(selling_case.aging)
        self.assertIsNone(selling_case.grade)
        self.assertIsNone(selling_case.sale_mode)

    def test_same_selling_case_can_exist_for_different_products(self):
        second_product = Product.objects.create(
            name="Dior Homme",
        )

        second_oil_type = ProductType.objects.create(
            product=second_product,
            name=ProductType.OIL,
        )

        SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        second_case = SellingCase.objects.create(
            product_type=second_oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        self.assertIsNotNone(second_case.pk)

    def test_duplicate_selling_case_for_same_product_type_is_rejected(self):
        SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        with self.assertRaises(IntegrityError):
            SellingCase.objects.create(
                product_type=self.oil_type,
                aging=SellingCase.AGED,
                grade=2,
            )

    def test_oil_grade_must_be_positive(self):
        selling_case = SellingCase(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=0,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_oil_requires_aging_and_grade(self):
        selling_case = SellingCase(
            product_type=self.oil_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_commercial_requires_quality(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_commercial_cannot_use_aging(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
            quality=SellingCase.QUALITY_LOW,
            aging=SellingCase.AGED,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_original_requires_sale_mode(self):
        selling_case = SellingCase(
            product_type=self.original_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_original_cannot_use_quality(self):
        selling_case = SellingCase(
            product_type=self.original_type,
            sale_mode=SellingCase.FULL_BOTTLE,
            quality=SellingCase.QUALITY_LOW,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_standard_cannot_use_extra_attributes(self):
        selling_case = SellingCase(
            product_type=self.standard_type,
            quality=SellingCase.QUALITY_LOW,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()


class ProductTests(TestCase):
    def test_product_can_be_created(self):
        product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.assertEqual(product.name, "Dior Sauvage")


class ProductTypeTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

    def test_product_type_belongs_to_product(self):
        product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.assertEqual(product_type.product, self.product)


class MerchantProductTests(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

    def test_merchant_can_configure_product(self):
        merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.assertEqual(merchant_product.merchant, self.merchant)
        self.assertEqual(merchant_product.product, self.product)
        self.assertTrue(merchant_product.is_active)

    def test_same_product_cannot_be_configured_twice_for_same_merchant(self):
        MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        with self.assertRaises(IntegrityError):
            MerchantProduct.objects.create(
                merchant=self.merchant,
                product=self.product,
            )

    def test_merchant_can_deactivate_product(self):
        merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        merchant_product.is_active = False
        merchant_product.save()
        merchant_product.refresh_from_db()

        self.assertFalse(merchant_product.is_active)
        self.assertTrue(
            Product.objects.filter(pk=self.product.pk).exists()
        )


class MerchantProductTypeTests(TestCase):
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

    def test_merchant_can_configure_product_type(self):
        merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.oil_type,
        )

        self.assertEqual(
            merchant_product_type.merchant_product,
            self.merchant_product,
        )

        self.assertEqual(
            merchant_product_type.product_type,
            self.oil_type,
        )

        self.assertTrue(merchant_product_type.is_active)

    def test_same_product_type_cannot_be_configured_twice(self):
        MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.oil_type,
        )

        with self.assertRaises(IntegrityError):
            MerchantProductType.objects.create(
                merchant_product=self.merchant_product,
                product_type=self.oil_type,
            )

    def test_merchant_can_deactivate_product_type(self):
        merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.oil_type,
        )

        merchant_product_type.is_active = False
        merchant_product_type.save()
        merchant_product_type.refresh_from_db()

        self.assertFalse(merchant_product_type.is_active)
        self.assertTrue(
            ProductType.objects.filter(pk=self.oil_type.pk).exists()
        )


class MerchantSellingCaseTests(TestCase):
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

    def test_merchant_can_configure_selling_case(self):
        merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        self.assertEqual(
            merchant_selling_case.merchant_product_type,
            self.merchant_product_type,
        )

        self.assertEqual(
            merchant_selling_case.selling_case,
            self.selling_case,
        )

        self.assertTrue(merchant_selling_case.is_active)

    def test_same_selling_case_cannot_be_configured_twice(self):
        MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        with self.assertRaises(IntegrityError):
            MerchantSellingCase.objects.create(
                merchant_product_type=self.merchant_product_type,
                selling_case=self.selling_case,
            )

    def test_merchant_can_deactivate_selling_case(self):
        merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        merchant_selling_case.is_active = False
        merchant_selling_case.save()
        merchant_selling_case.refresh_from_db()

        self.assertFalse(merchant_selling_case.is_active)
        self.assertTrue(
            SellingCase.objects.filter(pk=self.selling_case.pk).exists()
        )

    def test_selling_case_must_belong_to_same_product_type(self):
        commercial_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.COMMERCIAL,
        )

        commercial_case = SellingCase.objects.create(
            product_type=commercial_type,
            quality=SellingCase.QUALITY_LOW,
        )

        with self.assertRaises(ValidationError):
            merchant_selling_case = MerchantSellingCase(
                merchant_product_type=self.merchant_product_type,
                selling_case=commercial_case,
            )
            merchant_selling_case.full_clean()

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