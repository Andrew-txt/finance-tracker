from decimal import Decimal
from typing import Dict
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from src.building_blocks.enum import CurrencyEnum


class CreateWalletDTO(BaseModel):
    name: str = Field(..., max_length=127)
    currency: CurrencyEnum 

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v


class WalletDTO(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    balance: Decimal
    currency: CurrencyEnum


class TotalBalanceDTO(BaseModel):
    currencies: Dict[CurrencyEnum, Decimal]


class UserWalletsDTO:
    wallets: list[WalletDTO]




