from django.test import TestCase

from modules.catalog.infrastructure.repositories.django_selling_case_repository import (
    DjangoSellingCaseRepository,
)
from modules.catalog.models import Product, ProductType, SellingCase


class DjangoSellingCaseRepositoryTests(TestCase):

    def test_list_returns_all_selling_cases(self):
        product = Product.objects.create(
            name="Dior Sauvage",
        )

        product_type = ProductType.objects.create(
            product=product,
            name="Commercial",
        )

        selling_case_1 = SellingCase.objects.create(
            product_type=product_type,
            name="Low",
        )

        selling_case_2 = SellingCase.objects.create(
            product_type=product_type,
            name="Medium",
        )

        repository = DjangoSellingCaseRepository()

        result = repository.list()

        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            result,
            [selling_case_1, selling_case_2],
        )