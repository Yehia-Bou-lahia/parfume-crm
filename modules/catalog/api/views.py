from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalog.api.serializers import (
    ConfigureGradeConfigurationSerializer,
    ConfigureMerchantProductSerializer,
    ConfigureMerchantProductTypeSerializer,
    GradeConfigurationSerializer,
    MerchantProductSerializer,
    MerchantProductTypeSerializer,
    ProductSerializer,
    ProductTypeSerializer,
    SellingCaseSerializer,
    ConfigureMerchantSellingCaseSerializer,
    MerchantSellingCaseSerializer,
    ConfigureMerchantSellingCasePricingSerializer,
    PricingSerializer,
)

from modules.catalog.application.exceptions import (
    MerchantNotFound,
    PricingAlreadyConfigured,
    ProductNotFound,
    MerchantProductAlreadyConfigured,
    MerchantProductNotFound,
    MerchantProductDoesNotBelongToMerchant,
    ProductTypeNotFound,
    ProductTypeDoesNotBelongToProduct,
    MerchantProductTypeAlreadyConfigured,
    MerchantProductTypeNotFound,
    MerchantProductTypeDoesNotBelongToMerchant,
    SellingCaseNotFound,
    SellingCaseDoesNotBelongToProductType,
    MerchantSellingCaseAlreadyConfigured,
    GradeConfigurationAlreadyConfigured,
    MerchantSellingCaseNotFound,
    MerchantSellingCaseDoesNotBelongToMerchant,
)

from modules.catalog.application.use_cases.configure_merchant_product import (
    ConfigureMerchantProductUseCase,
)

from modules.catalog.application.use_cases.configure_grade_configuration import (
    ConfigureGradeConfigurationUseCase,
)

from modules.catalog.application.use_cases.configure_merchant_selling_case import (
    ConfigureMerchantSellingCaseUseCase,
)

from modules.catalog.application.use_cases.configure_merchant_product_type import (
    ConfigureMerchantProductTypeUseCase,
)

from modules.catalog.application.use_cases.configure_merchant_selling_case_pricing import ConfigureMerchantSellingCasePricingUseCase
from modules.catalog.application.use_cases.list_product_types import (
    ListProductTypesUseCase,
)

from modules.catalog.application.use_cases.list_merchant_selling_cases import (
    ListMerchantSellingCasesUseCase,
)

from modules.catalog.application.use_cases.list_products import (
    ListProductsUseCase,
)

from modules.catalog.application.use_cases.list_selling_cases import (
    ListSellingCasesUseCase,
)

from modules.catalog.infrastructure.repositories.django_merchant_selling_case_repository import (
    DjangoMerchantSellingCaseRepository,
)

from modules.catalog.infrastructure.repositories.django_merchant_product_repository import (
    DjangoMerchantProductRepository,
)

from modules.catalog.infrastructure.repositories.django_merchant_product_type_repository import (
    DjangoMerchantProductTypeRepository,
)

from modules.catalog.infrastructure.repositories.django_grade_configuration_repository import (
    DjangoGradeConfigurationRepository,
)

from modules.catalog.infrastructure.repositories.django_pricing_repository import DjangoPricingRepository
from modules.catalog.infrastructure.repositories.django_product_repository import (
    DjangoProductRepository,
)

from modules.catalog.infrastructure.repositories.django_product_type_repository import (
    DjangoProductTypeRepository,
)

from modules.catalog.infrastructure.repositories.django_selling_case_repository import (
    DjangoSellingCaseRepository,
)

from modules.catalog.models.merchant_selling_case import MerchantSellingCase


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        repository = DjangoProductRepository()
        use_case = ListProductsUseCase(repository)
        return use_case.execute()


class ProductTypeListView(generics.ListAPIView):
    serializer_class = ProductTypeSerializer

    def get_queryset(self):
        repository = DjangoProductTypeRepository()
        use_case = ListProductTypesUseCase(repository)
        return use_case.execute()


class SellingCaseListView(generics.ListAPIView):
    serializer_class = SellingCaseSerializer

    def get_queryset(self):
        repository = DjangoSellingCaseRepository()
        use_case = ListSellingCasesUseCase(repository)
        return use_case.execute()


class ConfigureMerchantProductView(generics.CreateAPIView):
    serializer_class = ConfigureMerchantProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repository = DjangoMerchantProductRepository()

        use_case = ConfigureMerchantProductUseCase(
            repository
        )

        try:
            merchant_product = use_case.execute(
                merchant_id=kwargs["merchant_id"],
                product_id=serializer.validated_data["product_id"],
            )

        except MerchantNotFound:
            return Response(
                {"detail": "Merchant not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ProductNotFound:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except MerchantProductAlreadyConfigured:
            return Response(
                {
                    "detail": (
                        "Product is already configured "
                        "for this merchant."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        response_serializer = MerchantProductSerializer(
            merchant_product
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ConfigureMerchantProductTypeView(generics.CreateAPIView):
    serializer_class = ConfigureMerchantProductTypeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repository = DjangoMerchantProductTypeRepository()

        use_case = ConfigureMerchantProductTypeUseCase(
            repository
        )

        try:
            merchant_product_type = use_case.execute(
                merchant_id=kwargs["merchant_id"],
                merchant_product_id=kwargs["merchant_product_id"],
                product_type_id=serializer.validated_data[
                    "product_type_id"
                ],
            )
        except MerchantProductNotFound:
            return Response(
                {"detail": "Merchant product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MerchantProductDoesNotBelongToMerchant:
            return Response(
                {
                    "detail": (
                        "Merchant product does not belong "
                        "to this merchant."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except ProductTypeNotFound:
            return Response(
                {"detail": "Product type not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ProductTypeDoesNotBelongToProduct:
            return Response(
                {
                    "detail": (
                        "Product type does not belong "
                        "to this product."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except MerchantProductTypeAlreadyConfigured:
            return Response(
                {
                    "detail": (
                        "Product type is already configured "
                        "for this product."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        response_serializer = MerchantProductTypeSerializer(
            merchant_product_type
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ConfigureMerchantSellingCaseView(generics.CreateAPIView):
    serializer_class = ConfigureMerchantSellingCaseSerializer

    def get(self, request, *args, **kwargs):
        repository = DjangoMerchantSellingCaseRepository()

        use_case = ListMerchantSellingCasesUseCase(
            repository
        )

        try:
            merchant_selling_cases = use_case.execute(
                merchant_id=kwargs["merchant_id"],
                merchant_product_type_id=kwargs[
                    "merchant_product_type_id"
                ],
            )

        except MerchantProductTypeNotFound:
            return Response(
                {"detail": "Merchant product type not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except MerchantProductTypeDoesNotBelongToMerchant:
            return Response(
                {
                    "detail": (
                        "Merchant product type does not belong "
                        "to this merchant."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = MerchantSellingCaseSerializer(
            merchant_selling_cases,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repository = DjangoMerchantSellingCaseRepository()

        use_case = ConfigureMerchantSellingCaseUseCase(
            repository
        )

        try:
            merchant_selling_case = use_case.execute(
                merchant_id=kwargs["merchant_id"],
                merchant_product_type_id=kwargs[
                    "merchant_product_type_id"
                ],
                selling_case_id=serializer.validated_data[
                    "selling_case_id"
                ],
            )

        except MerchantProductTypeNotFound:
            return Response(
                {"detail": "Merchant product type not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except MerchantProductTypeDoesNotBelongToMerchant:
            return Response(
                {
                    "detail": (
                        "Merchant product type does not belong "
                        "to this merchant."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except SellingCaseNotFound:
            return Response(
                {"detail": "Selling case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except SellingCaseDoesNotBelongToProductType:
            return Response(
                {
                    "detail": (
                        "Selling case does not belong "
                        "to this product type."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except MerchantSellingCaseAlreadyConfigured:
            return Response(
                {
                    "detail": (
                        "Selling case is already configured "
                        "for this product type."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        response_serializer = MerchantSellingCaseSerializer(
            merchant_selling_case
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ConfigureGradeConfigurationView(APIView):
    def post(
        self,
        request,
        merchant_id,
        merchant_product_id,
        merchant_product_type_id,
        merchant_selling_case_id,
    ):
        serializer = ConfigureGradeConfigurationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        use_case = ConfigureGradeConfigurationUseCase(
            repository=DjangoGradeConfigurationRepository()
        )

        try:
            grade_configuration = use_case.execute(
                merchant_id=merchant_id,
                merchant_selling_case_id=merchant_selling_case_id,
                grade=serializer.validated_data["grade"],
            )

        except MerchantSellingCaseNotFound:
            return Response(
                {"detail": "Merchant selling case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except MerchantSellingCaseDoesNotBelongToMerchant:
            return Response(
                {"detail": "Merchant selling case does not belong to merchant."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except GradeConfigurationAlreadyConfigured:
            return Response(
                {"detail": "Grade is already configured."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            GradeConfigurationSerializer(grade_configuration).data,
            status=status.HTTP_201_CREATED,
        )


class ConfigureMerchantSellingCasePricingView(APIView):
    def post(
        self,
        request,
        merchant_id,
        merchant_product_id,
        merchant_product_type_id,
        merchant_selling_case_id,
    ):
        serializer = ConfigureMerchantSellingCasePricingSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        use_case = ConfigureMerchantSellingCasePricingUseCase(
            repository=DjangoPricingRepository()
        )

        try:
            pricing = use_case.execute(
                merchant_id=merchant_id,
                merchant_selling_case_id=merchant_selling_case_id,
                behavior=serializer.validated_data["behavior"],
                amount=serializer.validated_data.get("amount"),
                rate=serializer.validated_data.get("rate"),
            )

        except MerchantSellingCaseNotFound:
            return Response(
                {"detail": "Merchant selling case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except MerchantSellingCaseDoesNotBelongToMerchant:
            return Response(
                {"detail": "Merchant selling case does not belong to merchant."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except PricingAlreadyConfigured:
            return Response(
                {"detail": "Pricing is already configured."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            PricingSerializer(pricing).data,
            status=status.HTTP_201_CREATED,
        )