from uuid import UUID
from pydantic import BaseModel, Field, field_validator

class UserDTO(BaseModel):
    id: UUID
    name: str
    login: str


class CreateUserDTO(BaseModel):
    name: str
    login: str


