from django.urls import path

from modules.catalog.api.views import (
    ConfigureMerchantProductTypeView,
    ConfigureMerchantProductView,
    ConfigureMerchantSellingCaseView,
    ProductListView,
    ProductTypeListView,
    SellingCaseListView,
)
from .views import ConfigureGradeConfigurationView, ConfigureMerchantSellingCasePricingView

urlpatterns = [
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "product-types/",
        ProductTypeListView.as_view(),
        name="product-type-list",
    ),
    path(
        "selling-cases/",
        SellingCaseListView.as_view(),
        name="selling-case-list",
    ),
    path(
        "merchants/<int:merchant_id>/products/",
        ConfigureMerchantProductView.as_view(),
        name="merchant-product-configure",
    ),
    path(
        "merchants/<int:merchant_id>/products/<int:merchant_product_id>/types/",
        ConfigureMerchantProductTypeView.as_view(),
        name="merchant-product-type-configure",
    ),
    path(
        "merchants/<int:merchant_id>/products/<int:merchant_product_id>/types/<int:merchant_product_type_id>/selling-cases/",
        ConfigureMerchantSellingCaseView.as_view(),
        name="merchant-selling-case-configure",
    ),
    path(
        "merchants/<int:merchant_id>/products/<int:merchant_product_id>/types/<int:merchant_product_type_id>/selling-cases/<int:merchant_selling_case_id>/grades/",
        ConfigureGradeConfigurationView.as_view(),
        name="grade-configuration-create",
    ),
    path(
        "merchants/<int:merchant_id>/products/<int:merchant_product_id>/types/<int:merchant_product_type_id>/selling-cases/<int:merchant_selling_case_id>/pricing/",
        ConfigureMerchantSellingCasePricingView.as_view(),
        name="merchant-selling-case-pricing-create",
    ),
]