from modules.catalog.models import (
    MerchantProduct,
    MerchantProductType,
    ProductType,
)


class DjangoMerchantProductTypeRepository:

    def merchant_product_exists_by_id(
        self,
        merchant_product_id: int,
    ) -> bool:
        return MerchantProduct.objects.filter(
            pk=merchant_product_id,
        ).exists()

    def get_product_id(
        self,
        merchant_product_id: int,
    ) -> int:
        return MerchantProduct.objects.values_list(
            "product_id",
            flat=True,
        ).get(
            pk=merchant_product_id,
        )

    def product_type_exists_by_id(
        self,
        product_type_id: int,
    ) -> bool:
        return ProductType.objects.filter(
            pk=product_type_id,
        ).exists()

    def product_type_belongs_to_product(
        self,
        product_type_id: int,
        product_id: int,
    ) -> bool:
        return ProductType.objects.filter(
            pk=product_type_id,
            product_id=product_id,
        ).exists()

    def exists(
        self,
        merchant_product_id: int,
        product_type_id: int,
    ) -> bool:
        return MerchantProductType.objects.filter(
            merchant_product_id=merchant_product_id,
            product_type_id=product_type_id,
        ).exists()

    def create(
        self,
        merchant_product_id: int,
        product_type_id: int,
    ) -> MerchantProductType:
        return MerchantProductType.objects.create(
            merchant_product_id=merchant_product_id,
            product_type_id=product_type_id,
        )

    def merchant_product_belongs_to_merchant(
        self,
        merchant_product_id: int,
        merchant_id: int,
    ) -> bool:
        return MerchantProduct.objects.filter(
            pk=merchant_product_id,
            merchant_id=merchant_id,
        ).exists()