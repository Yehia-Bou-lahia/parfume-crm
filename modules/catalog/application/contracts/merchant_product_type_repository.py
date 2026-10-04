from typing import Protocol

from modules.catalog.models import MerchantProductType


class MerchantProductTypeRepository(Protocol):
    def merchant_product_exists_by_id(
        self,
        merchant_product_id: int,
    ) -> bool:
        ...

    def merchant_product_belongs_to_merchant(
        self,
        merchant_product_id: int,
        merchant_id: int,
    ) -> bool:
        ...

    def get_product_id(
        self,
        merchant_product_id: int,
    ) -> int:
        ...

    def product_type_exists_by_id(
        self,
        product_type_id: int,
    ) -> bool:
        ...

    def product_type_belongs_to_product(
        self,
        product_type_id: int,
        product_id: int,
    ) -> bool:
        ...

    def exists(
        self,
        merchant_product_id: int,
        product_type_id: int,
    ) -> bool:
        ...

    def create(
        self,
        merchant_product_id: int,
        product_type_id: int,
    ) -> MerchantProductType:
        ...