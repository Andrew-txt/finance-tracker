from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.users.application.dto import RefreshTokensPairDTO
from src.users.domain.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get(self, user_login: Optional[str] = None, user_id: Optional[UUID] = None) -> User | None:  
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_auth(self, sub: Optional[str] = None, user_id: Optional[UUID] = None) -> RefreshTokensPairDTO | None:
        pass

    @abstractmethod
    def check_if_refresh_token_exists(self, refresh_token: str) -> UUID | None:
        pass

    @abstractmethod
    def upsert_user_auth(self, user_auth_dto: RefreshTokensPairDTO) -> None:
        pass