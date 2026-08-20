from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserDTO(BaseModel):
    id: UUID
    name: str
    login: str


class CreateUserDTO(BaseModel):
    name: str
    login: str


class UserAuthDTO(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    
    sub: str
    user_id: UUID
    refresh_token: str


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
  