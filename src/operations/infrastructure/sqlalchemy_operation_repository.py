from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.building_blocks.enum import OperationType
from src.building_blocks.sqlalchemy_db_models import SQLAlchemyOperation
from src.operations.domain.operation import Operation, Transfer
from src.operations.domain.operation_repository import IOperationRepository


class SQLAlchemyOperationRepository(IOperationRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def _to_domain_entity(self, operation: SQLAlchemyOperation) -> Operation | Transfer:
        if operation.type == OperationType.TRANSFER:
            return Transfer(
                transfer_id=operation.id,
                wallet_id=operation.wallet_id, 
                amount=operation.amount, 
                currency=operation.currency, 
                destination_id=operation.destination_id,                    
                description=operation.description,
                created_at=operation.created_at
            )
        return Operation(
            operation_id=operation.id,
            wallet_id=operation.wallet_id, 
            type=operation.type,
            amount=operation.amount, 
            currency=operation.currency, 
            description=operation.description,
            created_at=operation.created_at
        )
    def _from_domain_entity(self, operation: Optional[Operation] = None, transfer: Optional[Transfer] = None) -> SQLAlchemyOperation: 
        if operation:
            return SQLAlchemyOperation(
                id=operation.id,
                wallet_id=operation.wallet_id, 
                type=operation.type,
                amount=operation.amount, 
                currency=operation.currency, 
                description=operation.description, 
                created_at=operation.created_at

            )
        if transfer:
            return SQLAlchemyOperation(
                id=transfer.id,
                wallet_id=transfer.wallet_id, 
                type=transfer.type,
                amount=transfer.amount, 
                currency=transfer.currency, 
                description=transfer.description,
                created_at=transfer.created_at,
                destination_id=transfer.destination_id
            )

    def get(self, operation_id: UUID) -> Operation | None:
        with self.session_factory() as session:
            repo_operation = session.query(SQLAlchemyOperation).filter(SQLAlchemyOperation.id == operation_id).scalar()

            if repo_operation:
                return self._to_domain_entity(repo_operation)
            
            return None
        
    def save(self, operation: Operation) -> Operation:
        repo_operation = self._from_domain_entity(operation=operation)
        
        with self.session_factory() as session:
            session.add(repo_operation)
            session.commit()
            return operation   
    
    def get_list(self, wallets_ids: list[UUID], date_from: datetime | None, date_to: datetime | None) -> list[Operation | Transfer] | None:
        with self.session_factory() as session:
            query = session.query(SQLAlchemyOperation).filter(SQLAlchemyOperation.wallet_id.in_(wallets_ids))

            if date_from:
                query = query.filter(SQLAlchemyOperation.created_at >= date_from)
            if date_to:
                query = query.filter(SQLAlchemyOperation.created_at <= date_to)

            operations = query.all()
            if operations: 
                list = [self._to_domain_entity(operation) for operation in operations]
                return list
            
            return None
        
