from django.test import SimpleTestCase, TestCase

from modules.catalog.application.exceptions import (
    MerchantNotFound,
    ProductNotFound,
    MerchantProductAlreadyConfigured,
)
from modules.catalog.application.use_cases.configure_merchant_product import (
    ConfigureMerchantProductUseCase,
)

from modules.catalog.infrastructure.repositories.django_merchant_product_repository import (
    DjangoMerchantProductRepository,
)
from modules.catalog.models import MerchantProduct, Product
from modules.merchants.models import Merchant

class FakeMerchantProductRepository:
    def __init__(
        self,
        merchant_exists=True,
        product_exists=True,
        already_configured=False,
    ):
        self.merchant_exists = merchant_exists
        self.product_exists = product_exists
        self.already_configured = already_configured
        self.created = None

    def merchant_exists_by_id(self, merchant_id):
        return self.merchant_exists

    def product_exists_by_id(self, product_id):
        return self.product_exists

    def exists(self, merchant_id, product_id):
        return self.already_configured

    def create(self, merchant_id, product_id):
        self.created = {
            "merchant_id": merchant_id,
            "product_id": product_id,
        }
        return self.created


class ConfigureMerchantProductUseCaseTests(SimpleTestCase):

    def test_configures_product_for_merchant(self):
        repository = FakeMerchantProductRepository()

        use_case = ConfigureMerchantProductUseCase(repository)

        result = use_case.execute(
            merchant_id=1,
            product_id=10,
        )

        self.assertEqual(
            result,
            {
                "merchant_id": 1,
                "product_id": 10,
            },
        )

        self.assertEqual(
            repository.created,
            {
                "merchant_id": 1,
                "product_id": 10,
            },
        )

    def test_raises_when_merchant_does_not_exist(self):
        repository = FakeMerchantProductRepository(
            merchant_exists=False,
        )

        use_case = ConfigureMerchantProductUseCase(repository)

        with self.assertRaises(MerchantNotFound):
            use_case.execute(
                merchant_id=999,
                product_id=10,
            )

    def test_raises_when_product_does_not_exist(self):
        repository = FakeMerchantProductRepository(
            product_exists=False,
        )

        use_case = ConfigureMerchantProductUseCase(repository)

        with self.assertRaises(ProductNotFound):
            use_case.execute(
                merchant_id=1,
                product_id=999,
            )

    def test_raises_when_product_is_already_configured(self):
        repository = FakeMerchantProductRepository(
            already_configured=True,
        )

        use_case = ConfigureMerchantProductUseCase(repository)

        with self.assertRaises(MerchantProductAlreadyConfigured):
            use_case.execute(
                merchant_id=1,
                product_id=10,
            )


class ConfigureMerchantProductIntegrationTests(TestCase):
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
        self.use_case = ConfigureMerchantProductUseCase(
            self.repository
        )

    def test_configures_product_in_database(self):
        result = self.use_case.execute(
            merchant_id=self.merchant.id,
            product_id=self.product.id,
        )

        self.assertIsInstance(
            result,
            MerchantProduct,
        )

        self.assertEqual(
            result.merchant_id,
            self.merchant.id,
        )

        self.assertEqual(
            result.product_id,
            self.product.id,
        )

        self.assertTrue(
            MerchantProduct.objects.filter(
                merchant=self.merchant,
                product=self.product,
            ).exists()
        )