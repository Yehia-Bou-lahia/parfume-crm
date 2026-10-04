from modules.catalog.application.contracts.product_type_repository import (
    ProductTypeRepository,
)
from modules.catalog.models import ProductType


class ListProductTypesUseCase:
    def __init__(self, repository: ProductTypeRepository):
        self.repository = repository

    def execute(self) -> list[ProductType]:
        return self.repository.list()