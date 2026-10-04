from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_pricing_repository import (
    DjangoPricingRepository,
)
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


class DjangoPricingRepositoryTests(TestCase):
    def setUp(self):
        self.repository = DjangoPricingRepository()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0555000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

    def test_merchant_selling_case_exists_by_id(self):
        self.assertTrue(
            self.repository.merchant_selling_case_exists_by_id(
                self.merchant_selling_case.id
            )
        )

        self.assertFalse(
            self.repository.merchant_selling_case_exists_by_id(999999)
        )

    def test_merchant_selling_case_belongs_to_merchant(self):
        self.assertTrue(
            self.repository.merchant_selling_case_belongs_to_merchant(
                merchant_selling_case_id=self.merchant_selling_case.id,
                merchant_id=self.merchant.id,
            )
        )

    def test_exists_for_merchant_selling_case(self):
        Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount="2500.00",
        )

        self.assertTrue(
            self.repository.exists_for_merchant_selling_case(
                self.merchant_selling_case.id
            )
        )

    def test_create_for_merchant_selling_case(self):
        pricing = self.repository.create_for_merchant_selling_case(
            merchant_selling_case_id=self.merchant_selling_case.id,
            behavior=Pricing.FIXED,
            amount="2500.00",
        )

        self.assertIsInstance(pricing, Pricing)

        self.assertEqual(
            pricing.merchant_selling_case_id,
            self.merchant_selling_case.id,
        )

        self.assertEqual(
            pricing.behavior,
            Pricing.FIXED,
        )

        self.assertEqual(
            pricing.amount,
            "2500.00",
        )