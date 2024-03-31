import os

from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str


settings = Settings()

email_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv('SMTP_USER'),
    MAIL_PASSWORD=os.getenv('SMTP_PASSWORD'),
    MAIL_FROM=os.getenv('SMTP_USER'),
    MAIL_PORT=os.getenv('SMTP_PORT'),
    MAIL_SERVER=os.getenv('SMTP_HOST'),
    MAIL_FROM_NAME="Your Name",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fast_mail = FastMail(email_config)
