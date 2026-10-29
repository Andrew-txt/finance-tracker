from typing import Any, Optional
from uuid import UUID, uuid4

class User:
    def __init__(self, user_id: UUID, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email
       

    @classmethod
    def create(cls, name: str, email: str):
        return cls(
            user_id=uuid4(), 
            name=name, 
            email=email
        ) 
    
    def format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    

