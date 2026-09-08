from abc import ABC, abstractmethod
from decimal import Decimal

from src.building_blocks.enum import CurrencyEnum


class IExternalSourceRatesProvider(ABC):
    @abstractmethod
    def get_rate(self, base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
        pass

    @abstractmethod
    def healthcheck(self) -> bool:
        pass
