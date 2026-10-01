from django.test import TestCase
from rest_framework.test import APIClient

from modules.catalog.models import Product, ProductType, SellingCase


class ProductListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name="Bleu de Chanel",
            description="Test perfume",
        )

    def test_product_list_returns_products(self):
        response = self.client.get("/api/catalog/products/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.product.id)
        self.assertEqual(data[0]["name"], "Bleu de Chanel")
        self.assertEqual(
            data[0]["description"],
            "Test perfume",
        )


class ProductTypeListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name="Bleu de Chanel",
            description="Test perfume",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Eau de Parfum",
        )

    def test_product_type_list_returns_product_types(self):
        response = self.client.get("/api/catalog/product-types/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.product_type.id)
        self.assertEqual(
            data[0]["product"],
            self.product.id,
        )
        self.assertEqual(
            data[0]["name"],
            "Eau de Parfum",
        )
