from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import Product, ProductType, SellingCase


class SellingCaseTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.oil_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.commercial_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.COMMERCIAL,
        )

        self.original_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.standard_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.STANDARD,
        )

    def test_oil_selling_case_stores_aging_and_grade(self):
        selling_case = SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        self.assertEqual(selling_case.product_type, self.oil_type)
        self.assertEqual(selling_case.aging, SellingCase.AGED)
        self.assertEqual(selling_case.grade, 2)

    def test_commercial_selling_case_stores_quality(self):
        selling_case = SellingCase.objects.create(
            product_type=self.commercial_type,
            quality=SellingCase.QUALITY_LOW,
        )

        self.assertEqual(selling_case.product_type, self.commercial_type)
        self.assertEqual(selling_case.quality, SellingCase.QUALITY_LOW)

    def test_original_selling_case_stores_sale_mode(self):
        selling_case = SellingCase.objects.create(
            product_type=self.original_type,
            sale_mode=SellingCase.FULL_BOTTLE,
        )

        self.assertEqual(selling_case.product_type, self.original_type)
        self.assertEqual(selling_case.sale_mode, SellingCase.FULL_BOTTLE)

    def test_standard_selling_case_has_no_extra_attributes(self):
        selling_case = SellingCase.objects.create(
            product_type=self.standard_type,
        )

        self.assertIsNone(selling_case.quality)
        self.assertIsNone(selling_case.aging)
        self.assertIsNone(selling_case.grade)
        self.assertIsNone(selling_case.sale_mode)

    def test_same_selling_case_can_exist_for_different_products(self):
        second_product = Product.objects.create(
            name="Dior Homme",
        )

        second_oil_type = ProductType.objects.create(
            product=second_product,
            name=ProductType.OIL,
        )

        SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        second_case = SellingCase.objects.create(
            product_type=second_oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        self.assertIsNotNone(second_case.pk)

    def test_duplicate_selling_case_for_same_product_type_is_rejected(self):
        SellingCase.objects.create(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=2,
        )

        with self.assertRaises(IntegrityError):
            SellingCase.objects.create(
                product_type=self.oil_type,
                aging=SellingCase.AGED,
                grade=2,
            )

    def test_oil_grade_must_be_positive(self):
        selling_case = SellingCase(
            product_type=self.oil_type,
            aging=SellingCase.AGED,
            grade=0,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_oil_requires_aging_and_grade(self):
        selling_case = SellingCase(
            product_type=self.oil_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_commercial_requires_quality(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_commercial_cannot_use_aging(self):
        selling_case = SellingCase(
            product_type=self.commercial_type,
            quality=SellingCase.QUALITY_LOW,
            aging=SellingCase.AGED,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_original_requires_sale_mode(self):
        selling_case = SellingCase(
            product_type=self.original_type,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_original_cannot_use_quality(self):
        selling_case = SellingCase(
            product_type=self.original_type,
            sale_mode=SellingCase.FULL_BOTTLE,
            quality=SellingCase.QUALITY_LOW,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()

    def test_standard_cannot_use_extra_attributes(self):
        selling_case = SellingCase(
            product_type=self.standard_type,
            quality=SellingCase.QUALITY_LOW,
        )

        with self.assertRaises(ValidationError):
            selling_case.full_clean()