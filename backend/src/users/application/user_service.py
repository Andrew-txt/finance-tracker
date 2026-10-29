import logging
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from src.building_blocks.jwt_service import JWTService
from src.building_blocks.errors import RepositoryError
from src.users.application.dto import CreateUserDTO, TokensPairDTO, RefreshTokensPairDTO, UserAuthDTO, UserDTO, UserDataDTO
from src.users.domain.user import User
from src.users.domain.user_repository import IUserRepository


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def authentificate_user(self, user_data: CreateUserDTO):
        if user_data.sub:
            # идем в базу. требуемый ответ - булево значение
            ...
            if not user_data.email: # если в базе отсутствует, проверку изменить
                user = User.create(name=user_data.name, email=user_data.email)
                self.repository.save(user)


    def create(self, user_data: CreateUserDTO) -> UserDTO:
        """
        Create user from dto and save it to repository.

        Args: 
            user_data (CreateUserDTO): user data from which to create User and save it.
        Returns:
            user_dto (UserDataDTO): user data with generated user_id.

        Raises:
            - 
        """

        user = User.create(name=user_data.name, email=user_data.email)
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
    def register_user(self, auth_data: UserAuthDTO) -> TokensPairDTO:
        """
        If user is not registered in system yet, save it and then refresh its tokens -> returns email, name, refresh and access token.
        If it is in system, change its email and then refresh its tokens if it is not valid --> returns email and name.
        """
        user_auth_in_db = self.repository.get_user_auth(sub=auth_data.sub)
        # logging.critical(f"USER_ID IN REGISTER: {user_id}")
        
        if user_auth_in_db: # fn пользователь существует
            user_dto = self.get(user_id=user_auth_in_db.user_id)
            
            if not JWTService.is_refresh_token_valid(user_auth_in_db.refresh_token): # fn пользователь существует и токен невалиден
                new_tokens = self._create_user_tokens_pair(data={"user_id": user_auth_in_db.user_id})
                return UserDataDTO(
                    id=user_dto.id,
                    name=user_dto.name,
                    email=user_dto.email,
                    refresh_token=new_tokens.refresh_token,
                    access_token=new_tokens.access_token
                )
            else: # fn пользователь существует и токен валиден
                return user_dto
            
        else: # fn пользователь не существует
            user = self.repository.save(self._create_domain_user(auth_data))
            # logging.critical(f"USER FORMED IN REGISTER: {user}")
            new_tokens = self._create_user_tokens_pair(data={"user_id": user.id})
            self.repository.upsert_user_auth(user_auth_dto=RefreshTokensPairDTO(user_id=user.id, refresh_token=new_tokens.refresh_token))

            return UserDataDTO(id=user.id, name=user.name, email=user.email, access_token=new_tokens.access_token, refresh_token=new_tokens.refresh_token)

        return None


    def refresh_access_token(self, refresh_token: str) -> TokensPairDTO | None: 
        # user_auth = self.repository.get_user_auth(user_id) 

        if JWTService.is_refresh_token_valid(refresh_token):
            user_id = self.repository.check_if_refresh_token_exists(refresh_token)
            if user_id:
                access_token = JWTService.create_access_token(data={"user_id": str(user_id)})

                # user_auth_dto = RefreshTokensPairDTO(sub=user_auth.sub, user_id=user_id, refresh_token=refresh_token)
                # self.repository.upsert_user_auth(user_auth_dto)

                return TokensPairDTO(access_token=access_token, refresh_token=refresh_token)

        return None # значит, refresh не валиден


    def _create_domain_user(self, user_auth_data: UserAuthDTO) -> User:
        return User.create(name=user_auth_data.name, email=user_auth_data.email)

    def _create_user_tokens_pair(data: dict, sub: str, user_id: str) -> TokensPairDTO:
        access_token = JWTService.create_access_token(data=data)
        refresh_token =  JWTService.create_refresh_token()

        tokens_dto = TokensPairDTO(refresh_token=refresh_token, access_token=access_token)


