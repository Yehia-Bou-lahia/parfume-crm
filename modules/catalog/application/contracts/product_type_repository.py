from typing import Protocol

from modules.catalog.models import ProductType


class ProductTypeRepository(Protocol):
    def list(self) -> list[ProductType]:
        ...