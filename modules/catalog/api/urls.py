from django.urls import path

from modules.catalog.api.views import (
    ProductListView,
    ProductTypeListView,
    SellingCaseListView,
)


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
]