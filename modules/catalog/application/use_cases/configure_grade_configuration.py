from modules.catalog.application.contracts.grade_configuration_repository import (
    GradeConfigurationRepository,
)
from modules.catalog.application.exceptions import (
    MerchantSellingCaseNotFound,
    MerchantSellingCaseDoesNotBelongToMerchant,
    GradeConfigurationAlreadyConfigured,
)


class ConfigureGradeConfigurationUseCase:
    def __init__(self, repository: GradeConfigurationRepository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        merchant_selling_case_id: int,
        grade: int,
    ):
        if not self.repository.merchant_selling_case_exists_by_id(
            merchant_selling_case_id
        ):
            raise MerchantSellingCaseNotFound

        if not self.repository.merchant_selling_case_belongs_to_merchant(
            merchant_selling_case_id=merchant_selling_case_id,
            merchant_id=merchant_id,
        ):
            raise MerchantSellingCaseDoesNotBelongToMerchant

        if self.repository.exists(
            merchant_selling_case_id=merchant_selling_case_id,
            grade=grade,
        ):
            raise GradeConfigurationAlreadyConfigured

        return self.repository.create(
            merchant_selling_case_id=merchant_selling_case_id,
            grade=grade,
        )