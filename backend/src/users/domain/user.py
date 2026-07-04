from typing import Any, Optional
from uuid import UUID, uuid4

class User:
    def __init__(self, user_id: UUID, name: str, login: str):
        self.id = user_id
        self.name = name
        self.login = login

    @classmethod
    def create(cls, name: str, login: str):
        return cls(
            user_id=uuid4(), 
            name=name, 
            login=login
            ) 
    
    def format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "login": self.login
        }
    

