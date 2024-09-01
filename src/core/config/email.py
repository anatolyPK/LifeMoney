import os

from fastapi_mail import ConnectionConfig, FastMail


email_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_USER"),
    MAIL_PORT=os.getenv("SMTP_PORT"),
    MAIL_SERVER=os.getenv("SMTP_HOST"),
    MAIL_FROM_NAME="Your Name",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fast_mail = FastMail(email_config)
