from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_product_repository import (
    DjangoProductRepository,
)
from modules.catalog.models import Product


class DjangoProductRepositoryTests(TestCase):

    def test_list_returns_all_products(self):
        product_1 = Product.objects.create(
            name="Dior Sauvage",
        )
        product_2 = Product.objects.create(
            name="Bleu de Chanel",
        )

        repository = DjangoProductRepository()

        result = repository.list()

        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            result,
            [product_1, product_2],
        )