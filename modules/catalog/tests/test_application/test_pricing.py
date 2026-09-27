from decimal import Decimal

from django.test import TestCase

from modules.catalog.application.use_cases.pricing import (
    configure_product_type,
    configure_selling_case,
)
from modules.catalog.models import (
    MerchantProductConfiguration,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


class ConfigureProductTypeTests(TestCase):
    def test_configures_standard_product_type_for_merchant(self):
        merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        product = Product.objects.create(
            name="Test Perfume",
        )

        product_type = ProductType.objects.create(
            product=product,
            name="Perfume",
        )

        configuration = configure_product_type(
            merchant=merchant,
            product_type=product_type,
            price=Decimal("2500.00"),
        )

        self.assertIsInstance(
            configuration,
            MerchantProductConfiguration,
        )

        self.assertEqual(
            configuration.merchant,
            merchant,
        )

        self.assertEqual(
            configuration.product_type,
            product_type,
        )

        self.assertEqual(
            configuration.price,
            Decimal("2500.00"),
        )


class ConfigureSellingCaseTests(TestCase):
    def test_configures_selling_case_for_merchant(self):
        merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        product = Product.objects.create(
            name="Test Perfume",
        )

        product_type = ProductType.objects.create(
            product=product,
            name="Perfume",
        )

        selling_case = SellingCase.objects.create(
            product_type=product_type,
            volume_ml=50,
        )

        configuration = configure_selling_case(
            merchant=merchant,
            selling_case=selling_case,
            price=Decimal("2500.00"),
        )

        self.assertIsInstance(
            configuration,
            MerchantSellingCase,
        )

        self.assertEqual(
            configuration.merchant,
            merchant,
        )

        self.assertEqual(
            configuration.selling_case,
            selling_case,
        )

        self.assertEqual(
            configuration.price,
            Decimal("2500.00"),
        )