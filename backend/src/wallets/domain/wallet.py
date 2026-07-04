from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from src.building_blocks.enum import CurrencyEnum
from src.building_blocks.errors import BusinessRuleViolationError


class Wallet:
    def __init__(self, wallet_id: UUID, user_id: UUID, name: str, balance: Decimal, currency: CurrencyEnum):
        self.id = wallet_id
        self.user_id = user_id
        self.name = name
        self._balance = balance 
        self.currency = currency

    @classmethod
    def create(cls, user_id: UUID, name: str, currency: CurrencyEnum):
        return cls(
            wallet_id=uuid4(),
            balance=Decimal(0),
            user_id=user_id, 
            name=name,
            currency=currency
        )

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value: Decimal) -> Decimal:  
        if value < 0:
            raise BusinessRuleViolationError("Balance cannot be less then zero")
        self._balance = value

    def format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "balance": self.balance,
            "currency": self.currency
        }