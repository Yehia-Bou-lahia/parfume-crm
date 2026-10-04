from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    MerchantSellingCase,
    Product,
    ProductType,
    SellingCase,
)
from modules.merchants.models import Merchant
from modules.catalog.models import GradeConfiguration

class GradeConfigurationTests(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.oil_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.OIL,
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.oil_type,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.oil_type,
            name="Aged",
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

    def test_grade_configuration_can_be_created(self):
        configuration = GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

        self.assertEqual(
            configuration.merchant_selling_case,
            self.merchant_selling_case,
        )
        self.assertEqual(configuration.grade, 1)


    def test_grade_is_required(self):
        configuration = GradeConfiguration(
            merchant_selling_case=self.merchant_selling_case,
        )

        with self.assertRaises(ValidationError):
            configuration.full_clean()


    def test_grade_must_be_positive(self):
        configuration = GradeConfiguration(
            merchant_selling_case=self.merchant_selling_case,
            grade=0,
        )

        with self.assertRaises(ValidationError):
            configuration.full_clean()


    def test_same_grade_cannot_be_configured_twice_for_same_selling_case(self):
        GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

        with self.assertRaises(IntegrityError):
            GradeConfiguration.objects.create(
                merchant_selling_case=self.merchant_selling_case,
                grade=1,
            )


    def test_non_contiguous_grades_are_allowed(self):
        GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

        configuration = GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=5,
        )

        self.assertEqual(configuration.grade, 5)