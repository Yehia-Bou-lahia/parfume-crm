from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import Product, ProductType, SellingCase


class SellingCaseTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.commercial_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.COMMERCIAL,
        )

        self.oil_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

    def test_selling_case_can_be_created(self):
        selling_case = SellingCase.objects.create(
            product_type=self.commercial_type,
            name="Low",
        )

        self.assertEqual(
            selling_case.product_type,
            self.commercial_type,
        )
        self.assertEqual(selling_case.name, "Low")

    def test_selling_case_requires_product_type(self):
        selling_case = SellingCase(
            name="Low",
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_selling_case_requires_name(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_same_name_can_exist_for_different_product_types(self):
        SellingCase.objects.create(
            product_type=self.commercial_type,
            name="Low",
        )

        oil_case = SellingCase.objects.create(
            product_type=self.oil_type,
            name="Low",
        )

        self.assertIsNotNone(oil_case.pk)

    def test_duplicate_selling_case_for_same_product_type_is_rejected(self):
        SellingCase.objects.create(
            product_type=self.commercial_type,
            name="Low",
        )

        with self.assertRaises(IntegrityError):
            SellingCase.objects.create(
                product_type=self.commercial_type,
                name="Low",
            )

    def test_selling_case_has_no_legacy_domain_fields(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
            name="Low",
        )

        self.assertFalse(hasattr(selling_case, "grade"))
        self.assertFalse(hasattr(selling_case, "quality"))
        self.assertFalse(hasattr(selling_case, "aging"))
        self.assertFalse(hasattr(selling_case, "sale_mode"))