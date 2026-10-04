from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_product_type_repository import (
    DjangoProductTypeRepository,
)
from modules.catalog.models import Product, ProductType


class DjangoProductTypeRepositoryTests(TestCase):

    def test_list_returns_all_product_types(self):
        product = Product.objects.create(
            name="Dior Sauvage",
        )

        product_type_1 = ProductType.objects.create(
            product=product,
            name="Original",
        )
        product_type_2 = ProductType.objects.create(
            product=product,
            name="Oil",
        )

        repository = DjangoProductTypeRepository()

        result = repository.list()

        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            result,
            [product_type_1, product_type_2],
        )