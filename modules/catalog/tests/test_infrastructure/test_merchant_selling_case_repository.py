from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_merchant_selling_case_repository import (
    DjangoMerchantSellingCaseRepository,
)
from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant


class DjangoMerchantSellingCaseRepositoryTests(TestCase):

    def setUp(self):
        self.repository = DjangoMerchantSellingCaseRepository()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.other_merchant = Merchant.objects.create(
            name="Another Merchant",
            phone="0550000001",
            address="Another Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.other_product = Product.objects.create(
            name="Chanel Bleu",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Original Bottle",
        )

        self.other_product_type = ProductType.objects.create(
            product=self.other_product,
            name="Original Bottle",
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.other_selling_case = SellingCase.objects.create(
            product_type=self.other_product_type,
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

    def test_merchant_product_type_exists(self):
        self.assertTrue(
            self.repository.merchant_product_type_exists_by_id(
                self.merchant_product_type.id
            )
        )

    def test_merchant_product_type_does_not_exist(self):
        self.assertFalse(
            self.repository.merchant_product_type_exists_by_id(
                999999
            )
        )

    def test_merchant_product_type_belongs_to_merchant(self):
        self.assertTrue(
            self.repository.merchant_product_type_belongs_to_merchant(
                merchant_product_type_id=self.merchant_product_type.id,
                merchant_id=self.merchant.id,
            )
        )

    def test_merchant_product_type_does_not_belong_to_another_merchant(self):
        self.assertFalse(
            self.repository.merchant_product_type_belongs_to_merchant(
                merchant_product_type_id=self.merchant_product_type.id,
                merchant_id=self.other_merchant.id,
            )
        )

    def test_selling_case_exists(self):
        self.assertTrue(
            self.repository.selling_case_exists_by_id(
                self.selling_case.id
            )
        )

    def test_selling_case_does_not_exist(self):
        self.assertFalse(
            self.repository.selling_case_exists_by_id(
                999999
            )
        )

    def test_selling_case_belongs_to_product_type(self):
        self.assertTrue(
            self.repository.selling_case_belongs_to_product_type(
                selling_case_id=self.selling_case.id,
                product_type_id=self.product_type.id,
            )
        )

    def test_selling_case_does_not_belong_to_another_product_type(self):
        self.assertFalse(
            self.repository.selling_case_belongs_to_product_type(
                selling_case_id=self.other_selling_case.id,
                product_type_id=self.product_type.id,
            )
        )

    def test_get_product_type_id(self):
        product_type_id = self.repository.get_product_type_id(
            self.merchant_product_type.id
        )

        self.assertEqual(
            product_type_id,
            self.product_type.id,
        )

    def test_exists_returns_false_before_configuration(self):
        self.assertFalse(
            self.repository.exists(
                merchant_product_type_id=self.merchant_product_type.id,
                selling_case_id=self.selling_case.id,
            )
        )

    def test_create_creates_merchant_selling_case(self):
        merchant_selling_case = self.repository.create(
            merchant_product_type_id=self.merchant_product_type.id,
            selling_case_id=self.selling_case.id,
        )

        self.assertEqual(
            merchant_selling_case.merchant_product_type_id,
            self.merchant_product_type.id,
        )

        self.assertEqual(
            merchant_selling_case.selling_case_id,
            self.selling_case.id,
        )

        self.assertTrue(
            merchant_selling_case.is_active
        )

    def test_exists_returns_true_after_configuration(self):
        self.repository.create(
            merchant_product_type_id=self.merchant_product_type.id,
            selling_case_id=self.selling_case.id,
        )

        self.assertTrue(
            self.repository.exists(
                merchant_product_type_id=self.merchant_product_type.id,
                selling_case_id=self.selling_case.id,
            )
        )