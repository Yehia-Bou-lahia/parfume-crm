from modules.catalog.application.contracts.selling_case_repository import (
    SellingCaseRepository,
)
from modules.catalog.models import SellingCase


class ListSellingCasesUseCase:
    def __init__(self, repository: SellingCaseRepository):
        self.repository = repository

    def execute(self) -> list[SellingCase]:
        return self.repository.list()