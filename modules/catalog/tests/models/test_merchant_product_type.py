from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    Product,
    ProductType,
)
from modules.merchants.models import Merchant


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