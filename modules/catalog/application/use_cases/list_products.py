from modules.catalog.application.contracts.product_repository import (
    ProductRepository,
)
from modules.catalog.models import Product


class ListProductsUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self) -> list[Product]:
        return self.repository.list()