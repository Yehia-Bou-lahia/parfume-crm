from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import MerchantProduct, Product
from modules.merchants.models import Merchant


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