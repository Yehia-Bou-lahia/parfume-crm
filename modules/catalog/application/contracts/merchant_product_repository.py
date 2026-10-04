from typing import Protocol

from modules.catalog.models import MerchantProduct


class MerchantProductRepository(Protocol):
    def merchant_exists_by_id(self, merchant_id: int) -> bool:
        ...

    def product_exists_by_id(self, product_id: int) -> bool:
        ...

    def exists(
        self,
        merchant_id: int,
        product_id: int,
    ) -> bool:
        ...

    def create(
        self,
        merchant_id: int,
        product_id: int,
    ) -> MerchantProduct:
        ...

    def merchant_product_belongs_to_merchant(
        self,
        merchant_product_id: int,
        merchant_id: int,
    ) -> bool:
        ...