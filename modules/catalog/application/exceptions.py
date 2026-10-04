
class MerchantNotFound(Exception):
    pass


class ProductNotFound(Exception):
    pass


class MerchantProductAlreadyConfigured(Exception):
    pass


class MerchantProductNotFound(Exception):
    pass


class ProductTypeNotFound(Exception):
    pass


class ProductTypeDoesNotBelongToProduct(Exception):
    pass


class MerchantProductTypeAlreadyConfigured(Exception):
    pass


class MerchantProductDoesNotBelongToMerchant(Exception):
    pass


class MerchantProductTypeNotFound(Exception):
    pass


class MerchantProductTypeDoesNotBelongToMerchant(Exception):
    pass


class SellingCaseNotFound(Exception):
    pass


class MerchantSellingCaseAlreadyConfigured(Exception):
    pass


class SellingCaseDoesNotBelongToProductType(Exception):
    pass


class MerchantSellingCaseNotFound(Exception):
    pass


class MerchantSellingCaseDoesNotBelongToMerchant(Exception):
    pass


class GradeConfigurationAlreadyConfigured(Exception):
    pass


class PricingAlreadyConfigured(Exception):
    pass