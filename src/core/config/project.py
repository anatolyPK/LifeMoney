from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from pydantic_settings import BaseSettings


load_dotenv()


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    reset_token_expire_minutes: int = 60

    TOKEN_TYPE_FIELD: str = "type"
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    RESET_TOKEN_TYPE: str = "reset"

    RESET_PASSWORD_TOKEN_AUDIENCE: str = "fastapi"


class Settings(BaseSettings):
    # HOST: str
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
