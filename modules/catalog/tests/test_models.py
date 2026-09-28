from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import (
    MerchantProductConfiguration,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


class MerchantProductConfigurationTests(TestCase):

    def test_cannot_configure_product_type_with_selling_cases(self):
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

        SellingCase.objects.create(
            product_type=product_type,
            volume_ml=50,
        )

        configuration = MerchantProductConfiguration(
            merchant=merchant,
            product_type=product_type,
            price=Decimal("2500.00"),
        )

        with self.assertRaises(ValidationError):
            configuration.full_clean()

    def test_can_configure_product_type_without_selling_cases(self):
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

        configuration = MerchantProductConfiguration(
            merchant=merchant,
            product_type=product_type,
            price=Decimal("2500.00"),
        )

        configuration.full_clean()

    def test_cannot_create_selling_case_when_product_type_is_configured(self):
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

        MerchantProductConfiguration.objects.create(
            merchant=merchant,
            product_type=product_type,
            price=Decimal("2500.00"),
        )

        selling_case = SellingCase(
            product_type=product_type,
            volume_ml=50,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()


class MerchantSellingCaseTests(TestCase):

    def test_merchant_can_configure_selling_case_price(self):
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

        configuration = MerchantSellingCase(
            merchant=merchant,
            selling_case=selling_case,
            price=Decimal("2500.00"),
        )

        configuration.full_clean()
        configuration.save()

        self.assertEqual(
            configuration.price,
            Decimal("2500.00"),
        )

    def test_merchant_cannot_configure_same_selling_case_twice(self):
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

        MerchantSellingCase.objects.create(
            merchant=merchant,
            selling_case=selling_case,
            price=Decimal("2500.00"),
        )

        with self.assertRaises(IntegrityError):
            MerchantSellingCase.objects.create(
                merchant=merchant,
                selling_case=selling_case,
                price=Decimal("3000.00"),
            )

    def test_merchant_cannot_configure_selling_case_when_product_type_is_configured(
        self,
    ):
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

        MerchantProductConfiguration.objects.create(
            merchant=merchant,
            product_type=product_type,
            price=Decimal("2500.00"),
        )

        selling_case = SellingCase.objects.create(
            product_type=product_type,
            volume_ml=50,
        )

        configuration = MerchantSellingCase(
            merchant=merchant,
            selling_case=selling_case,
            price=Decimal("3000.00"),
        )

        with self.assertRaises(ValidationError):
            configuration.full_clean()
