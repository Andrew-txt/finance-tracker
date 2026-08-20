from contextlib import AbstractContextManager
from typing import Callable, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.users.application.dto import UserAuthDTO
from src.building_blocks.sqlalchemy_db_models import SQLAlchemyUser, SQLAlchemyUserAuth

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
    
    def get(self, user_login: Optional[str] = None, user_id: Optional[UUID] = None) -> User | None: 
        with self.session_factory() as session:
            # logging.critical(f"RECEIVED USER ID IN GET IN REPO: {user_id}")
            if user_id:
                repo_user = session.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).scalar()
          
                # logging.critical(f"FOUND USER IN REPO: {repo_user}")

                if repo_user:
                    return self._to_domain_entity(user=repo_user)
                    
                else: 
                    # logging.critical(f"NO USER FOUND IN GET IN REPO") # убрать этот else так как в конце стоит return None и  убрать вообще login
                    return None
                
            elif user_login:
                repo_user = session.query(SQLAlchemyUser).filter(SQLAlchemyUser.login == user_login).scalar()
        return None

    def save(self, user: User) -> User:
        repo_user = self._from_domain_entity(user)

        with self.session_factory() as session:
            possible_user = self.get(user_login=repo_user.login)
            if possible_user:
                return possible_user
             
            session.add(repo_user)
            session.commit()
            return user  

    def get_user_auth(self, sub: Optional[str] = None, user_id: Optional[UUID] = None) -> UserAuthDTO | None:
        with self.session_factory() as session:
            if user_id: 
                user_auth = session.query(SQLAlchemyUserAuth).filter(SQLAlchemyUserAuth.user_id == user_id).scalar() 
            elif sub: 
                user_auth = session.query(SQLAlchemyUserAuth).filter(SQLAlchemyUserAuth.sub == sub).scalar()

        if user_auth:
            return UserAuthDTO.model_validate(user_auth)
        return None

    def check_if_refresh_token_exists(self, refresh_token: str) -> UUID | None:
        with self.session_factory() as session:
            user_creds = session.query(SQLAlchemyUserAuth.refresh_token, SQLAlchemyUserAuth.user_id).filter(SQLAlchemyUserAuth.refresh_token == refresh_token).scalar()

            if user_creds:
                return user_creds.user_id
            return None

    def upsert_user_auth(self, user_auth_dto: UserAuthDTO) -> None:
        user_auth = SQLAlchemyUserAuth(**user_auth_dto.model_dump())
        # logging.critical(f"USER AUTH ID IN UPSERT: {user_auth.user_id}")

        with self.session_factory() as session:
            session.merge(user_auth)
            session.commit()
        return None
