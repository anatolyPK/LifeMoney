from pathlib import Path

from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    RESET_TOKEN_EXPIRE_MINUTES: int

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

    TOKEN_TYPE_FIELD: str = "type"
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    RESET_TOKEN_TYPE: str = "reset"

    RESET_PASSWORD_TOKEN_AUDIENCE: str = "fastapi"


class ApiKeys(BaseSettings):
    API_KEY_CMC: str
    API_KEY_CG: str
    API_KEY_TINKOFF: str


class Redis(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_MAX_CONNECTIONS: int


class Settings(BaseSettings):
    # HOST: str
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: list = ["*"]

    auth_jwt: AuthJWT = AuthJWT()
    api_keys: ApiKeys = ApiKeys()
    redis: Redis = Redis()


settings = Settings()
