from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.building_blocks.di import Container, get_current_user_id, container
from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.application.user_service import UserService

router = APIRouter()


@router.post("/users", response_model=UserDTO)
def create_user(request: CreateUserDTO): 
    user_service = container.user_service()

    # if user_service.create(user_data=request):
    #     return JSONResponse(status_code=201, content={"message": "created successfully"})
    # else:
    #     return JSONResponse(status_code=404, content={"error": "not created"})
    
    return user_service.create(user_data=request)



@router.get("/users/me", response_model=UserDTO)
def get_current_user(request: Request):
    current_user_id = get_current_user_id(request=request)
    user_service = container.user_service()
    
    return user_service.get(user_id=current_user_id)


