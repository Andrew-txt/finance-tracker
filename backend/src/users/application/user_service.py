import logging
from typing import Optional
from uuid import UUID

from src.building_blocks.auth.jwt_service import JWTService
from src.building_blocks.errors import RepositoryError
from src.users.application.dto import CreateUserDTO, TokenDTO, UserAuthDTO, UserDTO
from src.users.domain.user import User
from src.users.domain.user_repository import IUserRepository


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create(self, user_data: CreateUserDTO) -> UserDTO:
        user = User.create(name=user_data.name, login=user_data.login)
        self.repository.save(user)

        return UserDTO(**user.format())
    
    def get(self, user_id: Optional[UUID] = None, user_login: Optional[UUID] = None) -> UserDTO | None: 
        if user_id:
            user = self.repository.get(user_id=user_id) 
        elif user_login:
            user =  self.repository.get(user_login=user_login)
            
        if user: 
            return UserDTO(**user.format()) 
        else:
            return None

 # проблема заключалась в том что в register_user user_id в SQLAlchemyUserAuth есть, но в  SQLAlchemyUser -- нет, что приводит к неконсистентности и вызывает неправильную обработку метода format у доменных моделей pydantic моделями
    def register_user(self, auth_data: dict) -> TokenDTO:
        user_id = self.repository.get_user_auth(sub=auth_data.get("sub")).user_id # ID
        # logging.critical(f"USER_ID IN REGISTER: {user_id}")
        
        if not user_id:
            user = self.repository.save(self._create_domain_user(auth_data))
            # logging.critical(f"USER FORMED IN REGISTER: {user}")

            user_id = user.id

        access_token = JWTService.create_access_token(data={"user_id": str(user_id)})
        refresh_token =  JWTService.create_refresh_token()
        
        user_auth_dto = UserAuthDTO(sub=auth_data.get("sub"), user_id=user_id, refresh_token=refresh_token)
        self.repository.upsert_user_auth(user_auth_dto)

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)


    def refresh_access_token(self, refresh_token: str) -> TokenDTO | None: 
        # user_auth = self.repository.get_user_auth(user_id) 

        if JWTService.is_refresh_token_valid(refresh_token):
            user_id = self.repository.check_if_refresh_token_exists(refresh_token)
            if user_id:
                access_token = JWTService.create_access_token(data={"user_id": str(user_id)})

                # user_auth_dto = UserAuthDTO(sub=user_auth.sub, user_id=user_id, refresh_token=refresh_token)
                # self.repository.upsert_user_auth(user_auth_dto)

                return TokenDTO(access_token=access_token, refresh_token=refresh_token)

        return None # значит, refresh не валиден


    def _create_domain_user(self, user_auth_data: dict) -> User:
        return User.create(name=user_auth_data["name"], login=user_auth_data.get("email"))
            
