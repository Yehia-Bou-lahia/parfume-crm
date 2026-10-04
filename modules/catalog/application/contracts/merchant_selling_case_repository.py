
from typing import Protocol

from modules.catalog.models import MerchantSellingCase


class MerchantSellingCaseRepository(Protocol):
    def merchant_product_type_exists_by_id(
        self,
        merchant_product_type_id: int,
    ) -> bool:
        ...

    def merchant_product_type_belongs_to_merchant(
        self,
        merchant_product_type_id: int,
        merchant_id: int,
    ) -> bool:
        ...

    def selling_case_exists_by_id(
        self,
        selling_case_id: int,
    ) -> bool:
        ...

    def selling_case_belongs_to_product_type(
        self,
        selling_case_id: int,
        product_type_id: int,
    ) -> bool:
        ...

    def get_product_type_id(
        self,
        merchant_product_type_id: int,
    ) -> int:
        ...

    def exists(
        self,
        merchant_product_type_id: int,
        selling_case_id: int,
    ) -> bool:
        ...

    def create(
        self,
        merchant_product_type_id: int,
        selling_case_id: int,
    ) -> MerchantSellingCase:
        ...

    def list_by_merchant_product_type(
        self,
        merchant_product_type_id: int,
    ) -> list[MerchantSellingCase]:
        ...