from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from src.operations.application.operation_service import OperationService
from src.users.application.user_service import UserService
from src.wallets.application.wallet_service import WalletService

from src.operations.infrastructure.sqlalchemy_operation_repository import SQLAlchemyOperationRepository
from src.users.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.wallets.infrastructure.sqlalchemy_wallet_repository import SQLAlchemyWalletRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=['./config.yaml'])

    db_engine = providers.Singleton(
        create_engine,
        url=config.db.url,
        connect_args=config.db.connect_args
    )

    db_session_factory = providers.Singleton(  
        sessionmaker,
        autocommit=config.db.session.autocommit,
        autoflush=config.db.session.autoflush,
        bind=db_engine
    )

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session_factory=db_session_factory
    )

    operation_repository = providers.Factory(
        SQLAlchemyOperationRepository,
        session_factory=db_session_factory
    )

    wallet_repository = providers.Factory(
        SQLAlchemyWalletRepository,
        session_factory=db_session_factory
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )

    operation_service = providers.Factory(
        OperationService,
        repository=operation_repository,
        wallet_repository=wallet_repository
    )

    wallet_service = providers.Factory(
        WalletService,
        repository=wallet_repository
    )


security = HTTPBearer()

@inject
def get_current_user_id(request: Request, user_service: Annotated[UserService, Depends(Provide[Container.user_service])]):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Unauthorized")
    credentials = auth_header.replace("Bearer ", "")
    
    user = user_service.get(user_login=credentials)
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user.id
