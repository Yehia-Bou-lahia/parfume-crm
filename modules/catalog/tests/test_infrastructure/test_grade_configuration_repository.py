from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_grade_configuration_repository import (
    DjangoGradeConfigurationRepository,
)
from modules.catalog.models import (
    GradeConfiguration,
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


class DjangoGradeConfigurationRepositoryTests(TestCase):
    def setUp(self):
        self.repository = DjangoGradeConfigurationRepository()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0555000000",
            address="Test Address",
        )

        self.other_merchant = Merchant.objects.create(
            name="Other Merchant",
            phone="0666000000",
            address="Other Address",
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

        self.assertFalse(
            self.repository.merchant_selling_case_belongs_to_merchant(
                merchant_selling_case_id=self.merchant_selling_case.id,
                merchant_id=self.other_merchant.id,
            )
        )

    def test_exists(self):
        GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

        self.assertTrue(
            self.repository.exists(
                merchant_selling_case_id=self.merchant_selling_case.id,
                grade=1,
            )
        )

        self.assertFalse(
            self.repository.exists(
                merchant_selling_case_id=self.merchant_selling_case.id,
                grade=2,
            )
        )

    def test_create(self):
        grade_configuration = self.repository.create(
            merchant_selling_case_id=self.merchant_selling_case.id,
            grade=1,
        )

        self.assertIsInstance(
            grade_configuration,
            GradeConfiguration,
        )

        self.assertEqual(
            grade_configuration.merchant_selling_case_id,
            self.merchant_selling_case.id,
        )

        self.assertEqual(
            grade_configuration.grade,
            1,
        )