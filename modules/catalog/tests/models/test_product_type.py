from django.test import TestCase

from modules.catalog.models import Product, ProductType


class ProductTypeTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

    def test_product_type_belongs_to_product(self):
        product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.assertEqual(product_type.product, self.product)