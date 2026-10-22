
from django.contrib.auth import get_user_model
from django.http import request
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request

from modules.identity.models import MerchantMembership
from modules.identity.permissions import (
    HasActiveMerchantMembership,
    HasMerchantRole,
)
from modules.merchants.models import Merchant


class MerchantPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.owner = User.objects.create_user(
            username="owner",
            password="StrongPassword123!",
        )
        self.employee = User.objects.create_user(
            username="employee",
            password="StrongPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="StrongPassword123!",
        )

        self.merchant = Merchant.objects.create(
            name="Test Store",
            phone="0550000000",
            address="Algeria",
        )

        MerchantMembership.objects.create(
            user=self.owner,
            merchant=self.merchant,
            role=MerchantMembership.Role.OWNER,
        )
        MerchantMembership.objects.create(
            user=self.employee,
            merchant=self.merchant,
            role=MerchantMembership.Role.EMPLOYEE,
        )

        self.factory = APIRequestFactory()

    def make_view(self, user, roles=None):
        request = self.factory.post(
            f"/api/catalog/merchants/{self.merchant.pk}/products/"
        )
        if user is not None:
            force_authenticate(request, user=user)
        request = Request(request)

        if user is not None:
            request._user = user

        class DummyView:
            kwargs = {"merchant_id": self.merchant.pk}
            required_merchant_roles = roles or ()

        return request, DummyView()

    def test_active_member_can_access_merchant(self):
        request, view = self.make_view(self.employee)

        self.assertTrue(
            HasActiveMerchantMembership().has_permission(request, view)
        )

    def test_non_member_cannot_access_merchant(self):
        request, view = self.make_view(self.other_user)

        self.assertFalse(
            HasActiveMerchantMembership().has_permission(request, view)
        )

    def test_inactive_membership_cannot_access_merchant(self):
        membership = MerchantMembership.objects.get(
            user=self.employee,
            merchant=self.merchant,
        )
        membership.is_active = False
        membership.save(update_fields=["is_active"])

        request, view = self.make_view(self.employee)

        self.assertFalse(
            HasActiveMerchantMembership().has_permission(request, view)
        )

    def test_owner_role_is_required_when_configured(self):
        request, view = self.make_view(
            self.employee,
            roles=[MerchantMembership.Role.OWNER],
        )

        self.assertFalse(HasMerchantRole().has_permission(request, view))

    def test_owner_can_pass_owner_role_check(self):
        request, view = self.make_view(
            self.owner,
            roles=[MerchantMembership.Role.OWNER],
        )

        self.assertTrue(HasMerchantRole().has_permission(request, view))
