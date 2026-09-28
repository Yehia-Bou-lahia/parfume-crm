from django.urls import path

from modules.catalog.api.views import (
    ProductListView,
    ProductTypeListView,
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
]