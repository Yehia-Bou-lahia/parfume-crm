from django.test import TestCase

from modules.catalog.models import Product


class ProductTests(TestCase):
    def test_product_can_be_created(self):
        product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.assertEqual(product.name, "Dior Sauvage")