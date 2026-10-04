from modules.catalog.application.exceptions import (
    MerchantProductNotFound,
    MerchantProductDoesNotBelongToMerchant,
    ProductTypeNotFound,
    ProductTypeDoesNotBelongToProduct,
    MerchantProductTypeAlreadyConfigured,
)


class ConfigureMerchantProductTypeUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        merchant_product_id: int,
        product_type_id: int,
    ):
        if not self.repository.merchant_product_exists_by_id(
            merchant_product_id
        ):
            raise MerchantProductNotFound

        if not self.repository.merchant_product_belongs_to_merchant(
            merchant_product_id=merchant_product_id,
            merchant_id=merchant_id,
        ):
            raise MerchantProductDoesNotBelongToMerchant

        if not self.repository.product_type_exists_by_id(
            product_type_id
        ):
            raise ProductTypeNotFound

        product_id = self.repository.get_product_id(
            merchant_product_id
        )

        if not self.repository.product_type_belongs_to_product(
            product_type_id=product_type_id,
            product_id=product_id,
        ):
            raise ProductTypeDoesNotBelongToProduct

        if self.repository.exists(
            merchant_product_id=merchant_product_id,
            product_type_id=product_type_id,
        ):
            raise MerchantProductTypeAlreadyConfigured

        return self.repository.create(
            merchant_product_id=merchant_product_id,
            product_type_id=product_type_id,
        )