from modules.catalog.models import (
    GradeConfiguration,
    MerchantSellingCase,
)


class DjangoGradeConfigurationRepository:
    def merchant_selling_case_exists_by_id(
        self,
        merchant_selling_case_id: int,
    ) -> bool:
        return MerchantSellingCase.objects.filter(
            pk=merchant_selling_case_id
        ).exists()

    def merchant_selling_case_belongs_to_merchant(
        self,
        merchant_selling_case_id: int,
        merchant_id: int,
    ) -> bool:
        return MerchantSellingCase.objects.filter(
            pk=merchant_selling_case_id,
            merchant_product_type__merchant_product__merchant_id=merchant_id,
        ).exists()

    def exists(
        self,
        merchant_selling_case_id: int,
        grade: int,
    ) -> bool:
        return GradeConfiguration.objects.filter(
            merchant_selling_case_id=merchant_selling_case_id,
            grade=grade,
        ).exists()

    def create(
        self,
        merchant_selling_case_id: int,
        grade: int,
    ) -> GradeConfiguration:
        return GradeConfiguration.objects.create(
            merchant_selling_case_id=merchant_selling_case_id,
            grade=grade,
        )