from unittest import TestCase
from unittest.mock import Mock

from modules.catalog.application.exceptions import (
    GradeConfigurationAlreadyConfigured,
    MerchantSellingCaseDoesNotBelongToMerchant,
    MerchantSellingCaseNotFound,
)
from modules.catalog.application.use_cases.configure_grade_configuration import (
    ConfigureGradeConfigurationUseCase,
)


class ConfigureGradeConfigurationUseCaseTests(TestCase):
    def setUp(self):
        self.repository = Mock()
        self.use_case = ConfigureGradeConfigurationUseCase(
            repository=self.repository
        )

    def test_raises_when_merchant_selling_case_does_not_exist(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = False

        with self.assertRaises(MerchantSellingCaseNotFound):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                grade=1,
            )

        self.repository.merchant_selling_case_belongs_to_merchant.assert_not_called()
        self.repository.exists.assert_not_called()
        self.repository.create.assert_not_called()

    def test_raises_when_merchant_selling_case_does_not_belong_to_merchant(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = False

        with self.assertRaises(MerchantSellingCaseDoesNotBelongToMerchant):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                grade=1,
            )

        self.repository.exists.assert_not_called()
        self.repository.create.assert_not_called()

    def test_raises_when_grade_is_already_configured(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = True
        self.repository.exists.return_value = True

        with self.assertRaises(GradeConfigurationAlreadyConfigured):
            self.use_case.execute(
                merchant_id=1,
                merchant_selling_case_id=10,
                grade=1,
            )

        self.repository.create.assert_not_called()

    def test_creates_grade_configuration(self):
        self.repository.merchant_selling_case_exists_by_id.return_value = True
        self.repository.merchant_selling_case_belongs_to_merchant.return_value = True
        self.repository.exists.return_value = False

        expected = object()
        self.repository.create.return_value = expected

        result = self.use_case.execute(
            merchant_id=1,
            merchant_selling_case_id=10,
            grade=1,
        )

        self.assertIs(result, expected)

        self.repository.create.assert_called_once_with(
            merchant_selling_case_id=10,
            grade=1,
        )