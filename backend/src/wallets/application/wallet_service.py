from decimal import Decimal
from uuid import UUID

from src.building_blocks.errors import RepositoryError
from src.building_blocks.enum import CurrencyEnum

from src.wallets.application.dto import CreateWalletDTO, TotalBalanceDTO, WalletDTO
from src.wallets.domain.wallet import Wallet
from src.wallets.domain.wallet_repository import IWalletRepository


class WalletService:
    def __init__(self, repository: IWalletRepository):
        self.repository = repository

    def create(self, wallet_data: CreateWalletDTO, user_id: UUID) -> WalletDTO:
        if self.repository.is_exists(user_id=user_id, wallet_name=wallet_data.name):
            raise RepositoryError(f"Wallet {wallet_data.name} already exists")

        wallet = Wallet.create(
            user_id=user_id,
            name=wallet_data.name,
            currency=wallet_data.currency
            )
        self.repository.save(wallet)

        return WalletDTO(**wallet.format())
    
    def get_total_balance(self, user_id: UUID) -> TotalBalanceDTO:
        wallets = self.repository.get_all_wallets(user_id=user_id)

        currency = {
            CurrencyEnum.RUB: "rub",
            CurrencyEnum.USD: "usd",
            CurrencyEnum.EUR: "eur"
        }

        total_balance = {k: Decimal(0) for k in currency.values()}

        for wallet in wallets:
            total_balance[wallet.currency] += wallet.balance

        return TotalBalanceDTO(currencies=total_balance)


    def get_all_wallets(self, user_id: UUID) -> list[WalletDTO]:
        wallets = self.repository.get_all_wallets(user_id=user_id)

        return [WalletDTO(**wallet.format()) for wallet in wallets]




