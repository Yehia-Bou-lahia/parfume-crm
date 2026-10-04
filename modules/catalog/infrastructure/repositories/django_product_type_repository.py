from modules.catalog.application.contracts.product_type_repository import (
    ProductTypeRepository,
)
from modules.catalog.models import ProductType


class DjangoProductTypeRepository:
    def list(self) -> list[ProductType]:
        return list(
            ProductType.objects.select_related("product")
        )