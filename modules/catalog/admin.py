from django.contrib import admin

from modules.catalog.models import Product, ProductType, SellingCase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name")


@admin.register(SellingCase)
class SellingCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "product_type", "volume_ml")