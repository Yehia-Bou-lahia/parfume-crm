
from django.test import SimpleTestCase

from modules.catalog.application.use_cases.list_products import (
    ListProductsUseCase,
)
from modules.catalog.models import Product


class FakeProductRepository:
    def __init__(self, products):
        self.products = products

    def list(self):
        return self.products


class ListProductsUseCaseTests(SimpleTestCase):
    def test_returns_products_from_repository(self):
        products = [
            Product(id=1, name="Dior Sauvage"),
            Product(id=2, name="Bleu de Chanel"),
        ]
        repository = FakeProductRepository(products)
        use_case = ListProductsUseCase(repository)

        result = use_case.execute()

        self.assertEqual(result, products)