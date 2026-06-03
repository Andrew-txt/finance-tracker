from abc import ABC, abstractmethod


class ICurrencyRates(ABC):
    @abstractmethod
    def get_exchange_rate(self, param: str):
        pass