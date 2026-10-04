from typing import Protocol

from modules.catalog.models import SellingCase


class SellingCaseRepository(Protocol):
    def list(self) -> list[SellingCase]:
        ...