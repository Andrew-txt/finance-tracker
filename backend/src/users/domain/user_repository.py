from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from .user import User


class IUserRepository(ABC):
    @abstractmethod
    def save() -> User:  
        pass

    @abstractmethod
    def get() -> User:  
        pass





