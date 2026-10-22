
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from modules.identity.models import MerchantMembership
from modules.merchants.models import Merchant


class MerchantMembershipTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="employee1",
            password="StrongPassword123!",
        )
        self.merchant = Merchant.objects.create(
            name="Test Perfume Store",
            phone="0550000000",
            address="Algeria",
        )

    def test_create_owner_membership(self):
        membership = MerchantMembership.objects.create(
            user=self.user,
            merchant=self.merchant,
            role=MerchantMembership.Role.OWNER,
        )

        self.assertEqual(membership.role, "OWNER")
        self.assertTrue(membership.is_active)

    def test_create_employee_membership(self):
        membership = MerchantMembership.objects.create(
            user=self.user,
            merchant=self.merchant,
            role=MerchantMembership.Role.EMPLOYEE,
        )

        self.assertEqual(membership.role, "EMPLOYEE")

    def test_same_user_cannot_have_duplicate_membership_in_same_merchant(self):
        MerchantMembership.objects.create(
            user=self.user,
            merchant=self.merchant,
            role=MerchantMembership.Role.EMPLOYEE,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MerchantMembership.objects.create(
                    user=self.user,
                    merchant=self.merchant,
                    role=MerchantMembership.Role.OWNER,
                )

    def test_user_can_belong_to_another_merchant(self):
        another_merchant = Merchant.objects.create(
            name="Another Store",
            phone="0660000000",
            address="Algeria",
        )

        first_membership = MerchantMembership.objects.create(
            user=self.user,
            merchant=self.merchant,
            role=MerchantMembership.Role.EMPLOYEE,
        )
        second_membership = MerchantMembership.objects.create(
            user=self.user,
            merchant=another_merchant,
            role=MerchantMembership.Role.OWNER,
        )

        self.assertNotEqual(
            first_membership.merchant_id,
            second_membership.merchant_id,
        )
