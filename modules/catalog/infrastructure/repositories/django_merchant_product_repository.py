from modules.catalog.application.contracts.merchant_product_repository import (
    MerchantProductRepository,
)
from modules.catalog.models import MerchantProduct
from modules.catalog.models import Product
from modules.merchants.models import Merchant


class DjangoMerchantProductRepository:
    def merchant_exists_by_id(self, merchant_id: int) -> bool:
        return Merchant.objects.filter(pk=merchant_id).exists()

    def product_exists_by_id(self, product_id: int) -> bool:
        return Product.objects.filter(pk=product_id).exists()

    def exists(
        self,
        merchant_id: int,
        product_id: int,
    ) -> bool:
        return MerchantProduct.objects.filter(
            merchant_id=merchant_id,
            product_id=product_id,
        ).exists()

    def create(
        self,
        merchant_id: int,
        product_id: int,
    ) -> MerchantProduct:
        return MerchantProduct.objects.create(
            merchant_id=merchant_id,
            product_id=product_id,
        )