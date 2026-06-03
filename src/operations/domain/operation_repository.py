from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.operations.domain.operation import Operation


class IOperationRepository(ABC):
    @abstractmethod
    def save(self, operation: Operation) -> Operation:  # | Transfer
        pass

    def get(self, operation_id: UUID) -> Operation:
        pass

    def get_list(self, wallets_ids: list[UUID], date_from: datetime | None, date_to: datetime | None) -> list[Operation]:
        pass