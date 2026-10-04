from modules.catalog.application.contracts.merchant_selling_case_repository import (
    MerchantSellingCaseRepository,
)
from modules.catalog.application.exceptions import (
    MerchantProductTypeNotFound,
    MerchantProductTypeDoesNotBelongToMerchant,
)


class ListMerchantSellingCasesUseCase:
    def __init__(self, repository: MerchantSellingCaseRepository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        merchant_product_type_id: int,
    ):
        if not self.repository.merchant_product_type_exists_by_id(
            merchant_product_type_id
        ):
            raise MerchantProductTypeNotFound

        if not self.repository.merchant_product_type_belongs_to_merchant(
            merchant_product_type_id=merchant_product_type_id,
            merchant_id=merchant_id,
        ):
            raise MerchantProductTypeDoesNotBelongToMerchant

        return self.repository.list_by_merchant_product_type(
            merchant_product_type_id=merchant_product_type_id,
        )