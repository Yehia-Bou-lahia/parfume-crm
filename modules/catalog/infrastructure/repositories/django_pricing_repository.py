from modules.catalog.models import (
    MerchantSellingCase,
    Pricing,
)


class DjangoPricingRepository:
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

    def exists_for_merchant_selling_case(
        self,
        merchant_selling_case_id: int,
    ) -> bool:
        return Pricing.objects.filter(
            merchant_selling_case_id=merchant_selling_case_id,
        ).exists()

    def create_for_merchant_selling_case(
        self,
        merchant_selling_case_id: int,
        behavior: str,
        amount=None,
        rate=None,
    ) -> Pricing:
        return Pricing.objects.create(
            merchant_selling_case_id=merchant_selling_case_id,
            behavior=behavior,
            amount=amount,
            rate=rate,
        )