
from typing import Protocol

from modules.catalog.models import Product


class ProductRepository(Protocol):
    def list(self) -> list[Product]:
        ...