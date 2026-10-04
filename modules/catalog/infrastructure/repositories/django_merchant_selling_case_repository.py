from modules.catalog.models import (
    MerchantProductType,
    MerchantSellingCase,
    SellingCase,
)


class DjangoMerchantSellingCaseRepository:
    def merchant_product_type_exists_by_id(
        self,
        merchant_product_type_id: int,
    ) -> bool:
        return MerchantProductType.objects.filter(
            pk=merchant_product_type_id
        ).exists()

    def merchant_product_type_belongs_to_merchant(
        self,
        merchant_product_type_id: int,
        merchant_id: int,
    ) -> bool:
        return MerchantProductType.objects.filter(
            pk=merchant_product_type_id,
            merchant_product__merchant_id=merchant_id,
        ).exists()

    def selling_case_exists_by_id(
        self,
        selling_case_id: int,
    ) -> bool:
        return SellingCase.objects.filter(
            pk=selling_case_id
        ).exists()

    def selling_case_belongs_to_product_type(
        self,
        selling_case_id: int,
        product_type_id: int,
    ) -> bool:
        return SellingCase.objects.filter(
            pk=selling_case_id,
            product_type_id=product_type_id,
        ).exists()

    def get_product_type_id(
        self,
        merchant_product_type_id: int,
    ) -> int:
        return MerchantProductType.objects.values_list(
            "product_type_id",
            flat=True,
        ).get(pk=merchant_product_type_id)

    def exists(
        self,
        merchant_product_type_id: int,
        selling_case_id: int,
    ) -> bool:
        return MerchantSellingCase.objects.filter(
            merchant_product_type_id=merchant_product_type_id,
            selling_case_id=selling_case_id,
        ).exists()

    def create(
        self,
        merchant_product_type_id: int,
        selling_case_id: int,
    ) -> MerchantSellingCase:
        return MerchantSellingCase.objects.create(
            merchant_product_type_id=merchant_product_type_id,
            selling_case_id=selling_case_id,
        )

    def list_by_merchant_product_type(
        self,
        merchant_product_type_id: int,
    ) -> list[MerchantSellingCase]:
        return list(
            MerchantSellingCase.objects.filter(
                merchant_product_type_id=merchant_product_type_id,
            ).select_related("selling_case")
        )
