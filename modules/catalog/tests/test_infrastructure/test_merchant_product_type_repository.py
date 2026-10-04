from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_merchant_product_type_repository import (
    DjangoMerchantProductTypeRepository,
)
from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    Product,
    ProductType,
)
from modules.merchants.models import Merchant


class DjangoMerchantProductTypeRepositoryTests(TestCase):

    def setUp(self):
        self.repository = DjangoMerchantProductTypeRepository()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
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

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

    def test_merchant_product_exists(self):
        self.assertTrue(
            self.repository.merchant_product_exists_by_id(
                self.merchant_product.id
            )
        )

    def test_merchant_product_does_not_exist(self):
        self.assertFalse(
            self.repository.merchant_product_exists_by_id(
                999999
            )
        )

    def test_get_product_id(self):
        product_id = self.repository.get_product_id(
            self.merchant_product.id
        )

        self.assertEqual(
            product_id,
            self.product.id,
        )

    def test_product_type_exists(self):
        self.assertTrue(
            self.repository.product_type_exists_by_id(
                self.product_type.id
            )
        )

    def test_product_type_does_not_exist(self):
        self.assertFalse(
            self.repository.product_type_exists_by_id(
                999999
            )
        )

    def test_product_type_belongs_to_product(self):
        self.assertTrue(
            self.repository.product_type_belongs_to_product(
                product_type_id=self.product_type.id,
                product_id=self.product.id,
            )
        )

    def test_product_type_does_not_belong_to_product(self):
        self.assertFalse(
            self.repository.product_type_belongs_to_product(
                product_type_id=self.other_product_type.id,
                product_id=self.product.id,
            )
        )

    def test_exists_returns_false_before_configuration(self):
        self.assertFalse(
            self.repository.exists(
                merchant_product_id=self.merchant_product.id,
                product_type_id=self.product_type.id,
            )
        )

    def test_create_creates_merchant_product_type(self):
        merchant_product_type = self.repository.create(
            merchant_product_id=self.merchant_product.id,
            product_type_id=self.product_type.id,
        )

        self.assertEqual(
            merchant_product_type.merchant_product_id,
            self.merchant_product.id,
        )
        self.assertEqual(
            merchant_product_type.product_type_id,
            self.product_type.id,
        )
        self.assertTrue(
            merchant_product_type.is_active
        )

    def test_exists_returns_true_after_configuration(self):
        self.repository.create(
            merchant_product_id=self.merchant_product.id,
            product_type_id=self.product_type.id,
        )

        self.assertTrue(
            self.repository.exists(
                merchant_product_id=self.merchant_product.id,
                product_type_id=self.product_type.id,
            )
        )

    def test_merchant_product_belongs_to_merchant(self):
        self.assertTrue(
            self.repository.merchant_product_belongs_to_merchant(
                merchant_product_id=self.merchant_product.id,
                merchant_id=self.merchant.id,
            )
        )


    def test_merchant_product_does_not_belong_to_another_merchant(self):
        another_merchant = Merchant.objects.create(
            name="Another Merchant",
            phone="0550000001",
            address="Another Address",
        )
    
        self.assertFalse(
            self.repository.merchant_product_belongs_to_merchant(
                merchant_product_id=self.merchant_product.id,
                merchant_id=another_merchant.id,
            )
        )