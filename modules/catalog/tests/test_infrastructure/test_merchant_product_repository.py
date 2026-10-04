from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_merchant_product_repository import (
    DjangoMerchantProductRepository,
)
from modules.catalog.models import MerchantProduct, Product
from modules.merchants.models import Merchant


class DjangoMerchantProductRepositoryTests(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.repository = DjangoMerchantProductRepository()

    def test_merchant_exists_by_id(self):
        self.assertTrue(
            self.repository.merchant_exists_by_id(
                self.merchant.id
            )
        )

    def test_merchant_does_not_exist_by_id(self):
        self.assertFalse(
            self.repository.merchant_exists_by_id(999)
        )

    def test_product_exists_by_id(self):
        self.assertTrue(
            self.repository.product_exists_by_id(
                self.product.id
            )
        )

    def test_product_does_not_exist_by_id(self):
        self.assertFalse(
            self.repository.product_exists_by_id(999)
        )

    def test_exists_returns_false_when_not_configured(self):
        self.assertFalse(
            self.repository.exists(
                self.merchant.id,
                self.product.id,
            )
        )

    def test_create_creates_merchant_product(self):
        merchant_product = self.repository.create(
            merchant_id=self.merchant.id,
            product_id=self.product.id,
        )

        self.assertIsInstance(
            merchant_product,
            MerchantProduct,
        )

        self.assertEqual(
            merchant_product.merchant_id,
            self.merchant.id,
        )

        self.assertEqual(
            merchant_product.product_id,
            self.product.id,
        )

        self.assertTrue(merchant_product.is_active)

    def test_exists_returns_true_after_create(self):
        self.repository.create(
            merchant_id=self.merchant.id,
            product_id=self.product.id,
        )

        self.assertTrue(
            self.repository.exists(
                self.merchant.id,
                self.product.id,
            )
        )