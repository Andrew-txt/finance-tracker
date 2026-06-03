from typing import Optional
from uuid import UUID

from src.building_blocks.errors import RepositoryError
from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.domain.user import User
from src.users.domain.user_repository import IUserRepository


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create(self, user_data: CreateUserDTO) -> UserDTO:
        user = User.create(name=user_data.name, login=user_data.login)

        self.repository.save(user)

        return UserDTO(**user.format())
    
    def get(self, user_id: Optional[UUID] = None, user_login: Optional[UUID] = None) -> UserDTO:
        if user_id is not None:
            return self.repository.get(user_id=user_id)
        else:
            return self.repository.get(user_login=user_login)
        
 