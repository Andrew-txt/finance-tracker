from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy import ForeignKey

from src.building_blocks.enum import CurrencyEnum, OperationType

Base = declarative_base()


class SQLAlchemyUser(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True) 
    name: Mapped[str]


class SQLAlchemyUserAuth(Base):
    __tablename__ = "user_auth"
    sub: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    refresh_token: Mapped[str]


class SQLAlchemyWallet(Base):
    __tablename__ = "wallet"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    currency: Mapped[CurrencyEnum]


class SQLAlchemyOperation(Base):
    __tablename__ = "operation"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    wallet_id: Mapped[UUID] = mapped_column(ForeignKey("wallet.id"), nullable=False)
    type: Mapped[OperationType]
    amount: Mapped[Decimal] 
    currency: Mapped[CurrencyEnum]
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now()) 
    destination_id: Mapped[UUID] = mapped_column(nullable=True)

