from django.test import TestCase

from modules.catalog.application.exceptions import (
    MerchantProductTypeNotFound,
    MerchantProductTypeDoesNotBelongToMerchant,
    SellingCaseNotFound,
    SellingCaseDoesNotBelongToProductType,
    MerchantSellingCaseAlreadyConfigured,
)
from modules.catalog.application.use_cases.configure_merchant_selling_case import (
    ConfigureMerchantSellingCaseUseCase,
)

from modules.catalog.application.use_cases.list_merchant_selling_cases import (
    ListMerchantSellingCasesUseCase,
)

from modules.catalog.models import MerchantSellingCase

class FakeMerchantSellingCaseRepository:

    def __init__(self):
        self.merchant_product_types = {
            1: 10,
        }

        self.selling_cases = {
            100: 10,
        }

        self.configured = set()
        self.created = []
        self.merchant_selling_cases = []

    def merchant_product_type_exists_by_id(
        self,
        merchant_product_type_id,
    ):
        return merchant_product_type_id in self.merchant_product_types

    def merchant_product_type_belongs_to_merchant(
        self,
        merchant_product_type_id,
        merchant_id,
    ):
        return merchant_id == 1

    def selling_case_exists_by_id(
        self,
        selling_case_id,
    ):
        return selling_case_id in self.selling_cases

    def selling_case_belongs_to_product_type(
        self,
        selling_case_id,
        product_type_id,
    ):
        return self.selling_cases.get(selling_case_id) == product_type_id

    def get_product_type_id(
        self,
        merchant_product_type_id,
    ):
        return self.merchant_product_types[
            merchant_product_type_id
        ]

    def exists(
        self,
        merchant_product_type_id,
        selling_case_id,
    ):
        return (
            merchant_product_type_id,
            selling_case_id,
        ) in self.configured

    def create(
        self,
        merchant_product_type_id,
        selling_case_id,
    ):
        self.configured.add(
            (
                merchant_product_type_id,
                selling_case_id,
            )
        )

        result = {
            "merchant_product_type_id": merchant_product_type_id,
            "selling_case_id": selling_case_id,
        }

        self.created.append(result)

        return result

    def list_by_merchant_product_type(
        self,
        merchant_product_type_id,
    ):
        return self.merchant_selling_cases


class ConfigureMerchantSellingCaseUseCaseTests(TestCase):

    def setUp(self):
        self.repository = FakeMerchantSellingCaseRepository()

        self.use_case = ConfigureMerchantSellingCaseUseCase(
            self.repository
        )

    def test_configures_selling_case(self):
        result = self.use_case.execute(
            merchant_id=1,
            merchant_product_type_id=1,
            selling_case_id=100,
        )

        self.assertEqual(
            result["merchant_product_type_id"],
            1,
        )

        self.assertEqual(
            result["selling_case_id"],
            100,
        )

    def test_raises_when_merchant_product_type_not_found(self):
        with self.assertRaises(
            MerchantProductTypeNotFound
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_type_id=999,
                selling_case_id=100,
            )

    def test_raises_when_merchant_product_type_does_not_belong_to_merchant(self):
        with self.assertRaises(
            MerchantProductTypeDoesNotBelongToMerchant
        ):
            self.use_case.execute(
                merchant_id=999,
                merchant_product_type_id=1,
                selling_case_id=100,
            )

    def test_raises_when_selling_case_not_found(self):
        with self.assertRaises(
            SellingCaseNotFound
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_type_id=1,
                selling_case_id=999,
            )

    def test_raises_when_selling_case_does_not_belong_to_product_type(self):
        self.repository.selling_cases[200] = 999

        with self.assertRaises(
            SellingCaseDoesNotBelongToProductType
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_type_id=1,
                selling_case_id=200,
            )

    def test_raises_when_selling_case_already_configured(self):
        self.repository.configured.add(
            (1, 100)
        )

        with self.assertRaises(
            MerchantSellingCaseAlreadyConfigured
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_type_id=1,
                selling_case_id=100,
            )


class ListMerchantSellingCasesUseCaseTests(TestCase):

    def setUp(self):
        self.repository = FakeMerchantSellingCaseRepository()

        self.repository.merchant_selling_cases = [
            MerchantSellingCase(id=1),
            MerchantSellingCase(id=2),
        ]

        self.use_case = ListMerchantSellingCasesUseCase(
            self.repository
        )

    def test_returns_merchant_selling_cases(self):
        result = self.use_case.execute(
            merchant_id=1,
            merchant_product_type_id=1,
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)

    def test_raises_when_merchant_product_type_not_found(self):
        with self.assertRaises(
            MerchantProductTypeNotFound
        ):
            self.use_case.execute(
                merchant_id=1,
                merchant_product_type_id=999,
            )

    def test_raises_when_merchant_product_type_does_not_belong_to_merchant(
        self,
    ):
        with self.assertRaises(
            MerchantProductTypeDoesNotBelongToMerchant
        ):
            self.use_case.execute(
                merchant_id=999,
                merchant_product_type_id=1,
            )