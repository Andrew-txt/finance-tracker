from contextlib import AbstractContextManager
from decimal import Decimal
from typing import Callable
from uuid import UUID
from sqlalchemy.orm import Session

from src.building_blocks.errors import RepositoryError
from src.building_blocks.sqlalchemy_db_models import SQLAlchemyWallet

from src.wallets.domain.wallet import Wallet
from src.wallets.domain.wallet_repository import IWalletRepository


class SQLAlchemyWalletRepository(IWalletRepository):
        def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]): 
            self.session_factory = session_factory
        
        def _to_domain_entity(self, wallet: SQLAlchemyWallet) -> Wallet:
            return Wallet(
            wallet_id=wallet.id,
            user_id=wallet.user_id,
            name=wallet.name,
            balance=wallet.balance, 
            currency=wallet.currency
        )
        
        def _from_domain_entity(self, wallet: Wallet) -> SQLAlchemyWallet:
            return SQLAlchemyWallet(
                id=wallet.id,
                name=wallet.name,
                balance=wallet.balance,
                user_id=wallet.user_id,
                currency=wallet.currency
            )

        def update_balance(self, balance: Decimal, wallet: Wallet) -> None:
            if balance < Decimal(0):
                raise RepositoryError("Balance cannot be less then zero")
            
            repo_wallet = self._from_domain_entity(wallet)
            repo_wallet.balance = balance
            
            with self.session_factory() as session:
                session.merge(repo_wallet)
                session.commit()
            
            return None

        def get(self, user_id: UUID, wallet_name: str) -> Wallet:
            with self.session_factory() as session:
                repo_wallet = session.query(SQLAlchemyWallet).filter(SQLAlchemyWallet.user_id == user_id, 
                                                                        SQLAlchemyWallet.name == wallet_name).scalar()
                if not repo_wallet:
                    raise RepositoryError("Not found")
                return self._to_domain_entity(repo_wallet)
            
        def get_all_wallets(self, user_id: UUID):
            with self.session_factory() as session:
                repo_wallets = session.query(SQLAlchemyWallet).filter(SQLAlchemyWallet.user_id == user_id).all()

                return [self._to_domain_entity(repo_wallet) for repo_wallet in repo_wallets]

        def is_exists(self, user_id: UUID, wallet_name: str) -> bool:
            with self.session_factory() as session:
                if session.query(SQLAlchemyWallet).filter(SQLAlchemyWallet.user_id == user_id, 
                                                            SQLAlchemyWallet.name == wallet_name).scalar():
                    return True
                
                return False
            
        def save(self, wallet: Wallet) -> None:
            repo_wallet = self._from_domain_entity(wallet)
            
            if self.is_exists(repo_wallet.user_id, repo_wallet.name):
                raise RepositoryError(f"Wallet {repo_wallet.name} already exists")
            
            with self.session_factory() as session:
                session.add(repo_wallet)
                session.commit()
                
                return None

             


