import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from src.building_blocks.di import Container, get_current_user_id
from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.application.user_service import UserService

router = APIRouter()


@router.post("/users", response_model=UserDTO)
@inject
def create_user(request: CreateUserDTO, user_service: Annotated[UserService, Depends(Provide[Container.user_service])]): 
    return user_service.create(user_data=request)


@router.get("/users/me", response_model=UserDTO)
@inject
def get_current_user(user_service: Annotated[UserService, Depends(Provide[Container.user_service])], current_user_id: UUID = Depends(get_current_user_id)):
    # logging.critical(f"USER_ID IN /ME CONTROLLER: {current_user_id}")

    user = user_service.get(user_id=current_user_id)
    
    # logging.critical(f"USER FOUND BY GET IN /ME: {user}")
    return user
