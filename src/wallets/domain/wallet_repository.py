from abc import ABC, abstractmethod
from uuid import UUID

from src.wallets.domain.wallet import Wallet

class IWalletRepository(ABC):
    @abstractmethod
    def save() -> ...:
        pass

    @abstractmethod
    def update_balance() -> None:
        pass 

    @abstractmethod
    def get() -> Wallet | None:
        pass

    @abstractmethod
    def get_all_wallets() -> list:
        pass

    @abstractmethod
    def is_exists() -> bool:
        pass