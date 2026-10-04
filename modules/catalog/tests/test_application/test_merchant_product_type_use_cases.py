from django.test import TestCase

from modules.catalog.application.exceptions import (
    MerchantProductDoesNotBelongToMerchant,
    MerchantProductNotFound,
    ProductTypeNotFound,
    ProductTypeDoesNotBelongToProduct,
    MerchantProductTypeAlreadyConfigured,
)
from modules.catalog.application.use_cases.configure_merchant_product_type import (
    ConfigureMerchantProductTypeUseCase,
)


class FakeMerchantProductTypeRepository:

    def __init__(self):
        self.merchant_products = {1: 10}
        self.product_types = {100}
        self.configured = set()
        self.created = []

    def merchant_product_exists_by_id(self, merchant_product_id):
        return merchant_product_id in self.merchant_products

    def get_product_id(self, merchant_product_id):
        return self.merchant_products[merchant_product_id]

    def product_type_exists_by_id(self, product_type_id):
        return product_type_id in self.product_types

    def product_type_belongs_to_product(
        self,
        product_type_id,
        product_id,
    ):
        return product_type_id == 100 and product_id == 10

    def exists(self, merchant_product_id, product_type_id):
        return (
            merchant_product_id,
            product_type_id,
        ) in self.configured

    def merchant_product_belongs_to_merchant(
        self,
        merchant_product_id,
        merchant_id,
    ):
        return merchant_id == 1

    def create(self, merchant_product_id, product_type_id):
        self.configured.add(
            (merchant_product_id, product_type_id)
        )

        result = {
            "merchant_product_id": merchant_product_id,
            "product_type_id": product_type_id,
        }

        self.created.append(result)

        return result


class ConfigureMerchantProductTypeUseCaseTests(TestCase):

    def setUp(self):
        self.repository = FakeMerchantProductTypeRepository()
        self.use_case = ConfigureMerchantProductTypeUseCase(
            self.repository
        )

    def test_configures_product_type(self):
        result = self.use_case.execute(
            merchant_id=1,
            merchant_product_id=1,
            product_type_id=100,
        )

        self.assertEqual(
            result["merchant_product_id"],
            1,
        )
        self.assertEqual(
            result["product_type_id"],
            100,
        )

    def test_raises_when_merchant_product_not_found(self):
        with self.assertRaises(MerchantProductNotFound):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_id=999,
                product_type_id=100,
            )

    def test_raises_when_product_type_not_found(self):
        with self.assertRaises(ProductTypeNotFound):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_id=1,
                product_type_id=999,
            )

    def test_raises_when_product_type_belongs_to_another_product(self):
        self.repository.product_types.add(200)

        with self.assertRaises(
            ProductTypeDoesNotBelongToProduct
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_id=1,
                product_type_id=200,
            )

    def test_raises_when_product_type_already_configured(self):
        self.repository.configured.add((1, 100))

        with self.assertRaises(
            MerchantProductTypeAlreadyConfigured
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_id=1,
                product_type_id=100,
            )

    def test_raises_when_merchant_product_does_not_belong_to_merchant(self):
        with self.assertRaises(
            MerchantProductDoesNotBelongToMerchant
        ):
            self.use_case.execute(
                merchant_id=999,
                merchant_product_id=1,
                product_type_id=100,
            )