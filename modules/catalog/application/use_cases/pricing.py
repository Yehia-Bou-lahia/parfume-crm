from modules.catalog.models import (
    MerchantProductConfiguration,
    MerchantSellingCase,
)


def configure_product_type(*, merchant, product_type, price):
    configuration = MerchantProductConfiguration(
        merchant=merchant,
        product_type=product_type,
        price=price,
    )

    configuration.full_clean()
    configuration.save()

    return configuration


def configure_selling_case(*, merchant, selling_case, price):
    configuration = MerchantSellingCase(
        merchant=merchant,
        selling_case=selling_case,
        price=price,
    )

    configuration.full_clean()
    configuration.save()

    return configuration
