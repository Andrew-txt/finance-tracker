from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateUserDTO(BaseModel): 
    # Либо password либо sub, вместе - нельзя или отсутсвие их вместе - нельзя. Поля name и email обязательны вместе 
    name: str
    email: str
    password: str
    sub: str



class RefreshTokensPairDTO(BaseModel): 
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    refresh_token: str


class TokensPairDTO(BaseModel): # fn будет выдаваться при обновлении токенов с помощью access_token 
    access_token: str
    refresh_token: str


class UserDTO(BaseModel): # fn будет выдаваться при запросе данных пользователя
    id: UUID
    name: str
    email: str


class UserAuthDTO(UserDTO): # fn будет отдаваться на вход UserService
    sub: str


class UserDataDTO(TokensPairDTO, UserDTO): # fn будет выдавается ли единоразово, при регистрации пользователя
    pass





