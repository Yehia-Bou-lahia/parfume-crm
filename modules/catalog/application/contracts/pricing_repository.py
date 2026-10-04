from typing import Protocol

from modules.catalog.models import Pricing


class PricingRepository(Protocol):
    def merchant_selling_case_exists_by_id(
        self,
        merchant_selling_case_id: int,
    ) -> bool:
        ...

    def merchant_selling_case_belongs_to_merchant(
        self,
        merchant_selling_case_id: int,
        merchant_id: int,
    ) -> bool:
        ...

    def exists_for_merchant_selling_case(
        self,
        merchant_selling_case_id: int,
    ) -> bool:
        ...

    def create_for_merchant_selling_case(
        self,
        merchant_selling_case_id: int,
        behavior: str,
        amount=None,
        rate=None,
    ) -> Pricing:
        ...