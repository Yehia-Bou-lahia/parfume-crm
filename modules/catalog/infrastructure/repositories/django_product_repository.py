
from modules.catalog.application.contracts.product_repository import (
    ProductRepository,
)
from modules.catalog.models import Product


class DjangoProductRepository:
    def list(self) -> list[Product]:
        return list(Product.objects.all())