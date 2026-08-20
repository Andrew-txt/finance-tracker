import urllib
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int 

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env") 

settings = Settings()


def generate_redirect_google_uri():
    query_params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost/profile",
        "response_type": "code",
        "scope": " ".join([
            "openid",
            "email",
            "profile"
        ]),
        "access_type": "offline",
    }
    query_str = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    return f"{base_url}?{query_str}"

