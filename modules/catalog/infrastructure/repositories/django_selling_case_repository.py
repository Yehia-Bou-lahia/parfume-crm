from modules.catalog.application.contracts.selling_case_repository import (
    SellingCaseRepository,
)
from modules.catalog.models import SellingCase


class DjangoSellingCaseRepository:
    def list(self) -> list[SellingCase]:
        return list(
            SellingCase.objects.select_related("product_type")
        )