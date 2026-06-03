from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

from src.building_blocks.enum import CurrencyEnum, OperationType


class CreateOperationDTO(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    type: OperationType
    amount: int
    description: str | None = Field(None, max_length=255)

    @field_validator("amount")
    def amount_not_negative(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v
    
    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v: 
            raise ValueError("Wallet name cannot be empty")
        return v
    

class CreateTransferDTO(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    destination_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator("destination_name")
    @classmethod
    def wallets_must_differ(cls, v: int, info) -> int:
        if "destination_name" in info.data and v == info.data["wallet_name"]:
            raise ValueError("Same wallets")
        return v
    

    @field_validator("amount")
    @classmethod
    def amount_not_negative(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v


class OperationDTO(BaseModel):
    id: UUID
    wallet_id: UUID
    type: OperationType
    amount: Decimal
    currency: CurrencyEnum
    destination_id: UUID | None = None
    created_at: datetime   
    description: str | None = None


class GetOperationStatisticsDTO(BaseModel):
    wallet_name: Optional[str] = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class OperationStatisticsDTO(BaseModel):
    wallet_name: str
    date_from: datetime | None = None
    date_to: datetime | None = None
    operations: List[OperationDTO]