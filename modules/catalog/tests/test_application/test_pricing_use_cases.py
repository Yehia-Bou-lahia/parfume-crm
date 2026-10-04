from unittest import TestCase
from unittest.mock import Mock

from modules.catalog.application.exceptions import (
    MerchantSellingCaseDoesNotBelongToMerchant,
    MerchantSellingCaseNotFound,
    PricingAlreadyConfigured,
)
from modules.catalog.application.use_cases.configure_merchant_selling_case_pricing import (
    ConfigureMerchantSellingCasePricingUseCase,
)


class ConfigureMerchantSellingCasePricingUseCaseTests(TestCase):
    def setUp(self):
        self.repository = Mock()
        self.use_case = ConfigureMerchantSellingCasePricingUseCase(
            repository=self.repository
        )

    def test_raises_when_merchant_selling_case_does_not_exist(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = False

        with self.assertRaises(MerchantSellingCaseNotFound):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                behavior="FIXED",
                amount="2500.00",
            )

        self.repository.merchant_selling_case_belongs_to_merchant.assert_not_called()
        self.repository.exists_for_merchant_selling_case.assert_not_called()
        self.repository.create_for_merchant_selling_case.assert_not_called()

    def test_raises_when_merchant_selling_case_does_not_belong_to_merchant(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = False

        with self.assertRaises(MerchantSellingCaseDoesNotBelongToMerchant):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                behavior="FIXED",
                amount="2500.00",
            )

        self.repository.exists_for_merchant_selling_case.assert_not_called()
        self.repository.create_for_merchant_selling_case.assert_not_called()

    def test_raises_when_pricing_already_exists(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = True
        self.repository.exists_for_merchant_selling_case.return_value = True

        with self.assertRaises(PricingAlreadyConfigured):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                behavior="FIXED",
                amount="2500.00",
            )

        self.repository.create_for_merchant_selling_case.assert_not_called()

    def test_creates_fixed_pricing(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = True
        self.repository.exists_for_merchant_selling_case.return_value = False

        expected = object()
        self.repository.create_for_merchant_selling_case.return_value = expected

        result = self.use_case.execute(
            merchant_id=1,
            merchant_selling_case_id=10,
            behavior="FIXED",
            amount="2500.00",
        )

        self.assertIs(result, expected)

        self.repository.create_for_merchant_selling_case.assert_called_once_with(
            merchant_selling_case_id=10,
            behavior="FIXED",
            amount="2500.00",
            rate=None,
        )

    def test_creates_per_volume_pricing(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = True
        self.repository.exists_for_merchant_selling_case.return_value = False

        expected = object()
        self.repository.create_for_merchant_selling_case.return_value = expected

        result = self.use_case.execute(
            merchant_id=1,
            merchant_selling_case_id=10,
            behavior="PER_VOLUME",
            rate="15.00",
        )

        self.assertIs(result, expected)

        self.repository.create_for_merchant_selling_case.assert_called_once_with(
            merchant_selling_case_id=10,
            behavior="PER_VOLUME",
            amount=None,
            rate="15.00",
        )