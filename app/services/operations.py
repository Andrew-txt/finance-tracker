from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.enum import OperationType
from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.repository import wallets as wallets_repository
from app.repository import operations as operations_repository
from fastapi import HTTPException
from app.database import SessionLocal
from app.services.exchange_service import get_exchange_rate


def add_income(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
        # subcaregory: str | None = None
    )

    db.commit()

    return OperationResponse.model_validate(operation)


def add_expense(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name) 
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.balance}"
        )
    
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.EXPENSE,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
        # subcaregory: str | None = None
    )

    db.commit()

    return OperationResponse.model_validate(operation)


def get_operations_list(
        db: Session,
        current_user: User,
        wallet_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
) -> list[OperationResponse]:
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet_id}' not found")
        
        wallets_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        wallets_ids = [w.id for w in wallets]

    operations = operations_repository.get_operation_list(db, wallets_ids, date_from, date_to)
    result = []

    for operation in operations:
        result.append(OperationResponse.model_validate(operation))

    return result


def transfer_between_wallets(
        db: Session, 
        current_user: User, 
        from_wallet_id: int, 
        to_wallet_id: int,
        amount: Decimal
) -> OperationResponse:
    from_wallet = wallets_repository.get_wallet_by_id(db, current_user.id, from_wallet_id)
    to_wallet = wallets_repository.get_wallet_by_id(db, current_user.id, to_wallet_id)

    if not from_wallet or not to_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if from_wallet.balance < amount:
        raise HTTPException(status_code=400, detail=f"Insufficient funds. Available: {from_wallet.balance}")
    
    target_amount = amount
    # exchange_rate = 1.0

    if from_wallet.currency != to_wallet.currency:
        exchange_rate = get_exchange_rate(from_wallet.currency, to_wallet.currency)
        target_amount = round(amount * exchange_rate, 2)

    from_wallet.balance = round(from_wallet.balance - amount, 2)
    to_wallet.balance = round(to_wallet.balance + target_amount, 2)

    operation = operations_repository.create_operation(
        db=db,
        wallet_id=from_wallet.id,
        type=OperationType.TRANSFER,
        amount=target_amount,
        currency=from_wallet.currency,
        category="Transfer"
    )
    db.add(from_wallet)
    db.add(to_wallet)
    db.add(operation)
    db.commit()
    
    return OperationResponse.model_validate(operation)