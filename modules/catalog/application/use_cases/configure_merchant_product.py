from modules.catalog.application.exceptions import (
    MerchantNotFound,
    ProductNotFound,
    MerchantProductAlreadyConfigured,
)


class ConfigureMerchantProductUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        merchant_id: int,
        product_id: int,
    ):
        if not self.repository.merchant_exists_by_id(merchant_id):
            raise MerchantNotFound

        if not self.repository.product_exists_by_id(product_id):
            raise ProductNotFound

        if self.repository.exists(merchant_id, product_id):
            raise MerchantProductAlreadyConfigured


        return self.repository.create(
            merchant_id=merchant_id,
            product_id=product_id,
        )