
from modules.catalog.application.contracts.merchant_selling_case_repository import (
    MerchantSellingCaseRepository,
)
from modules.catalog.application.exceptions import (
    MerchantProductTypeNotFound,
    MerchantProductTypeDoesNotBelongToMerchant,
    SellingCaseNotFound,
    SellingCaseDoesNotBelongToProductType,
    MerchantSellingCaseAlreadyConfigured,
)


class ConfigureMerchantSellingCaseUseCase:
    def __init__(self, repository: MerchantSellingCaseRepository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        merchant_product_type_id: int,
        selling_case_id: int,
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

        if not self.repository.selling_case_exists_by_id(
            selling_case_id
        ):
            raise SellingCaseNotFound

        product_type_id = self.repository.get_product_type_id(
            merchant_product_type_id
        )

        if not self.repository.selling_case_belongs_to_product_type(
            selling_case_id=selling_case_id,
            product_type_id=product_type_id,
        ):
            raise SellingCaseDoesNotBelongToProductType

        if self.repository.exists(
            merchant_product_type_id=merchant_product_type_id,
            selling_case_id=selling_case_id,
        ):
            raise MerchantSellingCaseAlreadyConfigured

        return self.repository.create(
            merchant_product_type_id=merchant_product_type_id,
            selling_case_id=selling_case_id,
        )