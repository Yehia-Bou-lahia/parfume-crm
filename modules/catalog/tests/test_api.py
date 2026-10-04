from django.test import TestCase
from rest_framework.test import APIClient
from modules.catalog.models.merchant_product_type import MerchantProductType
from modules.catalog.models.merchant_selling_case import MerchantSellingCase
from modules.catalog.models.grade_configuration import GradeConfiguration
from modules.catalog.models.pricing import Pricing
from modules.merchants.models import Merchant
from modules.catalog.models import (
    MerchantProduct,
    Product,
    ProductType,
    SellingCase
)


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


class SellingCaseListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name="Bleu de Chanel",
            description="Test perfume",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Commercial",
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Medium",
        )

    def test_selling_case_list_returns_selling_cases(self):
        response = self.client.get(
            "/api/catalog/selling-cases/"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["id"],
            self.selling_case.id,
        )
        self.assertEqual(
            data[0]["product_type"],
            self.product_type.id,
        )
        self.assertEqual(
            data[0]["name"],
            "Medium",
        )


class ConfigureMerchantProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
        )

    def test_merchant_can_configure_product(self):
        response = self.client.post(
            self.url,
            {"product_id": self.product.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        data = response.json()

        self.assertEqual(
            data["product_id"],
            self.product.id,
        )

        self.assertEqual(
            data["product_name"],
            "Dior Sauvage",
        )

        self.assertTrue(
            data["is_active"],
        )

        self.assertTrue(
            MerchantProduct.objects.filter(
                merchant=self.merchant,
                product=self.product,
            ).exists()
        )

    def test_returns_404_when_merchant_does_not_exist(self):
        response = self.client.post(
            "/api/catalog/merchants/999/products/",
            {"product_id": self.product.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Merchant not found.",
        )

    def test_returns_404_when_product_does_not_exist(self):
        response = self.client.post(
            self.url,
            {"product_id": 999},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Product not found.",
        )

    def test_returns_409_when_product_is_already_configured(self):
        MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        response = self.client.post(
            self.url,
            {"product_id": self.product.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            409,
        )

        self.assertEqual(
            response.json()["detail"],
            "Product is already configured for this merchant.",
        )

    def test_returns_400_when_product_id_is_missing(self):
        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )


    def test_returns_400_when_product_id_is_zero(self):
        response = self.client.post(
            self.url,
            {"product_id": 0},
            format="json",
        )
    
        self.assertEqual(
            response.status_code,
            400,
        )
    
    
    def test_returns_400_when_product_id_is_not_an_integer(self):
        response = self.client.post(
            self.url,
            {"product_id": "abc"},
            format="json",
        )
    
        self.assertEqual(
            response.status_code,
            400,
        )


class ConfigureMerchantProductTypeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.other_merchant = Merchant.objects.create(
            name="Other Merchant",
            phone="0550000001",
            address="Other Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.other_product = Product.objects.create(
            name="Bleu de Chanel",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Commercial",
        )

        self.other_product_type = ProductType.objects.create(
            product=self.other_product,
            name="Oil",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/"
        )

    def test_merchant_can_configure_product_type(self):
        response = self.client.post(
            self.url,
            {"product_type_id": self.product_type.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        data = response.json()

        self.assertEqual(
            data["product_type_id"],
            self.product_type.id,
        )

        self.assertEqual(
            data["product_type_name"],
            "Commercial",
        )

        self.assertTrue(
            data["is_active"],
        )

    def test_returns_404_when_merchant_product_does_not_exist(self):
        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/999/types/"
        )

        response = self.client.post(
            url,
            {"product_type_id": self.product_type.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Merchant product not found.",
        )

    def test_returns_403_when_merchant_product_belongs_to_another_merchant(self):
        other_merchant_product = MerchantProduct.objects.create(
            merchant=self.other_merchant,
            product=self.product,
        )

        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{other_merchant_product.id}/types/"
        )

        response = self.client.post(
            url,
            {"product_type_id": self.product_type.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertEqual(
            response.json()["detail"],
            "Merchant product does not belong to this merchant.",
        )

    def test_returns_404_when_product_type_does_not_exist(self):
        response = self.client.post(
            self.url,
            {"product_type_id": 999},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Product type not found.",
        )

    def test_returns_400_when_product_type_belongs_to_another_product(self):
        response = self.client.post(
            self.url,
            {"product_type_id": self.other_product_type.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            response.json()["detail"],
            "Product type does not belong to this product.",
        )

    def test_returns_409_when_product_type_is_already_configured(self):
        from modules.catalog.models import MerchantProductType

        MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        response = self.client.post(
            self.url,
            {"product_type_id": self.product_type.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            409,
        )

        self.assertEqual(
            response.json()["detail"],
            "Product type is already configured for this product.",
        )

    def test_returns_400_when_product_type_id_is_missing(self):
        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_returns_400_when_product_type_id_is_zero(self):
        response = self.client.post(
            self.url,
            {"product_type_id": 0},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_returns_400_when_product_type_id_is_not_an_integer(self):
        response = self.client.post(
            self.url,
            {"product_type_id": "abc"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )


class ConfigureMerchantSellingCaseAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.other_merchant = Merchant.objects.create(
            name="Other Merchant",
            phone="0550000001",
            address="Other Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.other_product = Product.objects.create(
            name="Bleu de Chanel",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Commercial",
        )

        self.other_product_type = ProductType.objects.create(
            product=self.other_product,
            name="Oil",
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.other_selling_case = SellingCase.objects.create(
            product_type=self.other_product_type,
            name="Full Bottle",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/"
            f"{self.merchant_product_type.id}/selling-cases/"
        )

    def test_merchant_can_configure_selling_case(self):
        response = self.client.post(
            self.url,
            {"selling_case_id": self.selling_case.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        data = response.json()

        self.assertEqual(
            data["selling_case_id"],
            self.selling_case.id,
        )

        self.assertEqual(
            data["selling_case_name"],
            "Full Bottle",
        )

        self.assertTrue(
            data["is_active"],
        )

    def test_returns_404_when_merchant_product_type_does_not_exist(self):
        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/999/selling-cases/"
        )

        response = self.client.post(
            url,
            {"selling_case_id": self.selling_case.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Merchant product type not found.",
        )

    def test_returns_403_when_merchant_product_type_belongs_to_another_merchant(
        self,
    ):
        other_merchant_product = MerchantProduct.objects.create(
            merchant=self.other_merchant,
            product=self.product,
        )

        other_merchant_product_type = MerchantProductType.objects.create(
            merchant_product=other_merchant_product,
            product_type=self.product_type,
        )

        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/"
            f"{other_merchant_product_type.id}/selling-cases/"
        )

        response = self.client.post(
            url,
            {"selling_case_id": self.selling_case.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertEqual(
            response.json()["detail"],
            "Merchant product type does not belong to this merchant.",
        )

    def test_returns_404_when_selling_case_does_not_exist(self):
        response = self.client.post(
            self.url,
            {"selling_case_id": 999},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(
            response.json()["detail"],
            "Selling case not found.",
        )

    def test_returns_400_when_selling_case_belongs_to_another_product_type(
        self,
    ):
        response = self.client.post(
            self.url,
            {"selling_case_id": self.other_selling_case.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            response.json()["detail"],
            "Selling case does not belong to this product type.",
        )

    def test_returns_409_when_selling_case_is_already_configured(self):
        MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        response = self.client.post(
            self.url,
            {"selling_case_id": self.selling_case.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            409,
        )

        self.assertEqual(
            response.json()["detail"],
            "Selling case is already configured for this product type.",
        )

    def test_returns_400_when_selling_case_id_is_missing(self):
        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_returns_400_when_selling_case_id_is_zero(self):
        response = self.client.post(
            self.url,
            {"selling_case_id": 0},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_returns_400_when_selling_case_id_is_not_an_integer(self):
        response = self.client.post(
            self.url,
            {"selling_case_id": "abc"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )


class MerchantSellingCaseListAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0550000000",
            address="Test Address",
        )

        self.other_merchant = Merchant.objects.create(
            name="Other Merchant",
            phone="0550000001",
            address="Other Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name="Commercial",
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/"
            f"{self.merchant_product_type.id}/selling-cases/"
        )

    def test_returns_merchant_selling_cases(self):
        MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["selling_case_id"],
            self.selling_case.id,
        )
        self.assertEqual(
            data[0]["selling_case_name"],
            "Full Bottle",
        )
        self.assertTrue(data[0]["is_active"])

    def test_returns_empty_list_when_no_selling_cases_are_configured(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_404_when_merchant_product_type_does_not_exist(self):
        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{self.merchant_product.id}/types/999/selling-cases/"
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["detail"],
            "Merchant product type not found.",
        )

    def test_returns_403_when_merchant_product_type_belongs_to_another_merchant(
        self,
    ):
        other_merchant_product = MerchantProduct.objects.create(
            merchant=self.other_merchant,
            product=self.product,
        )

        other_merchant_product_type = MerchantProductType.objects.create(
            merchant_product=other_merchant_product,
            product_type=self.product_type,
        )

        url = (
            f"/api/catalog/merchants/"
            f"{self.merchant.id}/products/"
            f"{other_merchant_product.id}/types/"
            f"{other_merchant_product_type.id}/selling-cases/"
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "Merchant product type does not belong to this merchant.",
        )


class ConfigureGradeConfigurationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0555000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        self.url = (
            f"/api/catalog/merchants/{self.merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            f"selling-cases/{self.merchant_selling_case.id}/"
            "grades/"
        )

    def test_can_configure_grade(self):
        response = self.client.post(
            self.url,
            {"grade": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.data["grade"],
            1,
        )

        self.assertTrue(
            GradeConfiguration.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
                grade=1,
            ).exists()
        )

    def test_grade_must_be_positive(self):
        response = self.client.post(
            self.url,
            {"grade": 0},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        self.assertFalse(
            GradeConfiguration.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
            ).exists()
        )

    def test_merchant_selling_case_must_belong_to_merchant(self):
        other_merchant = Merchant.objects.create(
            name="Other Merchant",
            phone="0666000000",
            address="Other Address",
        )

        url = (
            f"/api/catalog/merchants/{other_merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            f"selling-cases/{self.merchant_selling_case.id}/"
            "grades/"
        )

        response = self.client.post(
            url,
            {"grade": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            GradeConfiguration.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
                grade=1,
            ).exists()
        )

    def test_returns_404_when_merchant_selling_case_does_not_exist(self):
        url = (
            f"/api/catalog/merchants/{self.merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            "selling-cases/999999/grades/"
        )

        response = self.client.post(
            url,
            {"grade": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 404)


    def test_cannot_configure_same_grade_twice(self):
        GradeConfiguration.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            grade=1,
        )

        response = self.client.post(
            self.url,
            {"grade": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 409)

        self.assertEqual(
            GradeConfiguration.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
                grade=1,
            ).count(),
            1,
        )


    def test_can_configure_multiple_different_grades(self):
        response_1 = self.client.post(
            self.url,
            {"grade": 1},
            format="json",
        )

        response_2 = self.client.post(
            self.url,
            {"grade": 2},
            format="json",
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)

        self.assertEqual(
            GradeConfiguration.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
            ).count(),
            2,
        )


class ConfigureMerchantSellingCasePricingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(
            name="Test Merchant",
            phone="0555000000",
            address="Test Address",
        )

        self.product = Product.objects.create(
            name="Dior Sauvage",
        )

        self.product_type = ProductType.objects.create(
            product=self.product,
            name=ProductType.ORIGINAL,
        )

        self.selling_case = SellingCase.objects.create(
            product_type=self.product_type,
            name="Full Bottle",
        )

        self.merchant_product = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
        )

        self.merchant_product_type = MerchantProductType.objects.create(
            merchant_product=self.merchant_product,
            product_type=self.product_type,
        )

        self.merchant_selling_case = MerchantSellingCase.objects.create(
            merchant_product_type=self.merchant_product_type,
            selling_case=self.selling_case,
        )

        self.url = (
            f"/api/catalog/merchants/{self.merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            f"selling-cases/{self.merchant_selling_case.id}/"
            "pricing/"
        )

    def test_can_configure_fixed_pricing(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.FIXED,
                "amount": "2500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["behavior"], Pricing.FIXED)
        self.assertEqual(response.data["amount"], "2500.00")
        self.assertIsNone(response.data["rate"])

        self.assertTrue(
            Pricing.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
                behavior=Pricing.FIXED,
                amount="2500.00",
            ).exists()
        )

    def test_can_configure_per_volume_pricing(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.PER_VOLUME,
                "rate": "15.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["behavior"], Pricing.PER_VOLUME)
        self.assertEqual(response.data["rate"], "15.00")
        self.assertIsNone(response.data["amount"])

        self.assertTrue(
            Pricing.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
                behavior=Pricing.PER_VOLUME,
                rate="15.00",
            ).exists()
        )

    def test_fixed_pricing_requires_amount(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.FIXED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Pricing.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
            ).exists()
        )

    def test_fixed_pricing_cannot_have_rate(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.FIXED,
                "amount": "2500.00",
                "rate": "15.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_per_volume_pricing_requires_rate(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.PER_VOLUME,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_per_volume_pricing_cannot_have_amount(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.PER_VOLUME,
                "rate": "15.00",
                "amount": "2500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_amount_must_be_positive(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.FIXED,
                "amount": "0.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_rate_must_be_positive(self):
        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.PER_VOLUME,
                "rate": "0.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_behavior_is_rejected(self):
        response = self.client.post(
            self.url,
            {
                "behavior": "INVALID",
                "amount": "2500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_returns_404_when_merchant_selling_case_does_not_exist(self):
        url = (
            f"/api/catalog/merchants/{self.merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            "selling-cases/999999/pricing/"
        )

        response = self.client.post(
            url,
            {
                "behavior": Pricing.FIXED,
                "amount": "2500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_merchant_selling_case_must_belong_to_merchant(self):
        another_merchant = Merchant.objects.create(
            name="Another Merchant",
            phone="0666000000",
            address="Another Address",
        )

        url = (
            f"/api/catalog/merchants/{another_merchant.id}/"
            f"products/{self.merchant_product.id}/"
            f"types/{self.merchant_product_type.id}/"
            f"selling-cases/{self.merchant_selling_case.id}/pricing/"
        )

        response = self.client.post(
            url,
            {
                "behavior": Pricing.FIXED,
                "amount": "2500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_cannot_configure_pricing_twice(self):
        Pricing.objects.create(
            merchant_selling_case=self.merchant_selling_case,
            behavior=Pricing.FIXED,
            amount="2500.00",
        )

        response = self.client.post(
            self.url,
            {
                "behavior": Pricing.FIXED,
                "amount": "3000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 409)

        self.assertEqual(
            Pricing.objects.filter(
                merchant_selling_case=self.merchant_selling_case,
            ).count(),
            1,
        )