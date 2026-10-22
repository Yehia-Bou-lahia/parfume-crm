
from django.conf import settings
from django.db import models


class MerchantMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        EMPLOYEE = "EMPLOYEE", "Employee"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant_memberships",
    )
    merchant = models.ForeignKey(
        "merchants.Merchant",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "merchant"],
                name="unique_user_merchant_membership",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.merchant} ({self.role})"
