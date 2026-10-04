from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


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
            name="Aged",
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
            name="Low",
        )

        with self.assertRaises(ValidationError):
            merchant_selling_case = MerchantSellingCase(
                merchant_product_type=self.merchant_product_type,
                selling_case=commercial_case,
            )

            merchant_selling_case.full_clean()