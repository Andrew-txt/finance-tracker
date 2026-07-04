from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID, uuid4

from src.building_blocks.enum import CurrencyEnum, OperationType


class Operation:
    def __init__(self, operation_id, wallet_id, type, amount, currency, description, created_at):
        self.id = operation_id
        self.wallet_id = wallet_id   # или сразу принимать экземпляр Wallet?
        self.type = type
        self.amount = amount
        self.currency = currency
        self.description = description
        self.created_at = created_at   # или убрать эту крайнюю пару скобок/ выделить в метод

    @classmethod
    def create(cls, 
                wallet_id: UUID,
                type: str,  
                amount: Decimal,
                currency: CurrencyEnum,
                description: Optional[str]
                ):
        return cls(
            operation_id=uuid4(),
            wallet_id=wallet_id,
            type=type,
            amount=amount,
            currency=currency,
            description=description,
            created_at=datetime.now(timezone.utc)
        )

    def format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,         #потом как нибудь сделать по адекватному этот format чтобы столько не писать херни
            "type": self.type,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "created_at": self.created_at
        }

        
class Transfer(Operation):
    def __init__(self, transfer_id, wallet_id, amount, currency, description, destination_id, created_at):
        super().__init__(transfer_id, wallet_id, OperationType.TRANSFER, amount, currency, description, created_at)
        self.destination_id = destination_id

    @classmethod
    def create(cls,
                wallet_id: UUID, 
                amount: Decimal, 
                currency: CurrencyEnum, 
                destination_id: UUID,
                description: Optional[str]
            ):
        
        return Transfer(
            transfer_id=uuid4(),  # <--- айди кошелька с которого переводим
            wallet_id=wallet_id,
            amount=amount,
            currency=currency,
            destination_id=destination_id,
            description=description,
            created_at=datetime.now(timezone.utc)
            )
    
    def format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,         #потом как нибудь сделать по адекватному этот format чтобы столько не писать херни
            "type": self.type,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "created_at": self.created_at,
            "destination_id": self.destination_id
        }
