from modules.catalog.application.contracts.pricing_repository import (
    PricingRepository,
)
from modules.catalog.application.exceptions import (
    MerchantSellingCaseNotFound,
    MerchantSellingCaseDoesNotBelongToMerchant,
    PricingAlreadyConfigured,
)


class ConfigureMerchantSellingCasePricingUseCase:
    def __init__(self, repository: PricingRepository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        merchant_selling_case_id: int,
        behavior: str,
        amount=None,
        rate=None,
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

        if self.repository.exists_for_merchant_selling_case(
            merchant_selling_case_id
        ):
            raise PricingAlreadyConfigured

        return self.repository.create_for_merchant_selling_case(
            merchant_selling_case_id=merchant_selling_case_id,
            behavior=behavior,
            amount=amount,
            rate=rate,
        )