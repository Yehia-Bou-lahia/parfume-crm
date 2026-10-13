
from rest_framework.permissions import BasePermission

from modules.identity.models import MerchantMembership


class HasActiveMerchantMembership(BasePermission):
    """Require an active membership in the requested merchant."""

    message = "You do not have access to this merchant."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        merchant_id = view.kwargs.get("merchant_id")
        if merchant_id is None:
            return False

        return MerchantMembership.objects.filter(
            user=request.user,
            merchant_id=merchant_id,
            is_active=True,
        ).exists()


class HasMerchantRole(BasePermission):
    """Require an active membership with one of the allowed roles."""

    message = "Your role does not permit this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        merchant_id = view.kwargs.get("merchant_id")
        allowed_roles = getattr(view, "required_merchant_roles", ())

        if merchant_id is None or not allowed_roles:
            return False

        return MerchantMembership.objects.filter(
            user=request.user,
            merchant_id=merchant_id,
            is_active=True,
            role__in=allowed_roles,
        ).exists()
