import jwt

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.building_blocks.utils import settings
from src.users.application.dto import UserAuthDTO


class JWTService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else: 
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": expire})
        return jwt.encode(payload=data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    
    @staticmethod
    def create_refresh_token():
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        data = {
            "exp": expire,
            "jti": str(uuid4())
        }
        return jwt.encode(payload=data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        try:
            c = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return c
        except jwt.PyJWTError as e:
            # logging.critical(f"EXCEPTION {e.with_traceback}. CAUSED BY JWT TOKEN: {token}")
            return None

    @staticmethod
    def get_user_payload(token) -> UserAuthDTO:
        given_data = jwt.decode(
            token,
            algorithms=["RS256"],options={"verify_signature": False}
        )
        return UserAuthDTO(
            name=given_data["name"], 
            email=given_data["email"],
            sub=given_data["sub"]
        )
    
    @staticmethod
    def is_refresh_token_valid(refresh_token: str) -> bool:
        decoded = JWTService.decode_token(refresh_token)

        if decoded and decoded.get("exp") > datetime.now(timezone.utc):
            return True
        return False





            


