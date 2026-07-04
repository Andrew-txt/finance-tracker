from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.building_blocks.errors import RepositoryError
from src.building_blocks.sqlalchemy_db_models import SQLAlchemyUser

from src.users.domain.user import User
from src.users.domain.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def _to_domain_entity(self, user: SQLAlchemyUser) -> User:  
        return User(
            user_id=user.id,
            name=user.name,
            login=user.login
        )
    
    def _from_domain_entity(self, user: User) -> SQLAlchemyUser:
        return SQLAlchemyUser(
            id=user.id,
            login=user.login,
            name=user.name
        )
    
    def get(self, user_login: Optional[str] = None, user_id: Optional[UUID] = None) -> User | None: # user_id: Optional[Any] ######
        with self.session_factory() as session:
            if user_id is not None:
                repo_user = session.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).scalar()
            else:
                repo_user = session.query(SQLAlchemyUser).filter(SQLAlchemyUser.login == user_login).scalar()

            if not repo_user:
                return None
                # raise RepositoryError("User not found")
            
            return self._to_domain_entity(user=repo_user)
        

    def save(self, user: User) -> None:
        repo_user = self._from_domain_entity(user)

        with self.session_factory() as session:
            possible_user = self.get(user_login=repo_user.login)
            if possible_user:
                return None
             
                # raise RepositoryError("User already exists")
            session.add(repo_user)
            session.commit()
            return None   
    

