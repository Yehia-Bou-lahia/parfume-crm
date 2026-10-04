from typing import Protocol

from modules.catalog.models import GradeConfiguration


class GradeConfigurationRepository(Protocol):
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

    def exists(
        self,
        merchant_selling_case_id: int,
        grade: int,
    ) -> bool:
        ...

    def create(
        self,
        merchant_selling_case_id: int,
        grade: int,
    ) -> GradeConfiguration:
        ...