import aiohttp
import logging

from fastapi import Body, HTTPException, Query, APIRouter, status, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated

from dependency_injector.wiring import Provide, inject

from src.building_blocks.jwt_service import JWTService
from src.building_blocks.utils import generate_redirect_google_uri, settings
from src.building_blocks.di import Container

from src.users.application.dto import TokensPairDTO
from src.users.application.user_service import UserService

router = APIRouter(prefix="/google")


@router.get("/url")
def get_google_oauth_uri():
    uri = generate_redirect_google_uri()
    return RedirectResponse(uri, status_code=status.HTTP_302_FOUND)


@router.get("/tokens/access")
@inject
async def exchange_auth_code(user_service: Annotated[UserService, Depends(Provide[Container.user_service])], code: str = Query(...)):  
    google_token_url = "https://oauth2.googleapis.com/token"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=google_token_url,
            data={                                                
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost/profile",
                "code": code,
            }
        ) as response:
            res = await response.json()
            # logging.critical(f"JSON RECEIVED FROM GOOGLE: {res}")

            if res.get("error") and res.get("error") == "invalid_grant":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"error": "invalid_credentials", "description": "Invalid credentials"}
                )

            elif not res.get("id_token"):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail={"error": "unknown_error", "description": "Unknown error occurred"}
                )
            user_data = JWTService.get_user_payload(token=res.get("id_token")) 
            return user_service.register_user(user_data)

 
@router.post("/refresh", response_model=TokensPairDTO)
@inject
def refresh_access_token(user_service: Annotated[UserService, Depends(Provide[Container.user_service])], refresh_token: Annotated[str, Body(embed=True)]):
    tokens = user_service.refresh_access_token(refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"error": "invalid_credentials", "description": "Invalid credentials"}
        )
    return tokens