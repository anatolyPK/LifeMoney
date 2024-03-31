from fastapi_mail import MessageSchema
from pydantic import EmailStr
from fastapi import Request
from src.config.project_config import fast_mail


async def send_verification_email(email: EmailStr, token: str):
    verification_url = f"http://localhost:8000/auth/verify/?token={token}"
    template = f"""<html>
           <body>
               <p>Для подтверждения вашей учетной записи, пройдите по следующей ссылке:</p>
               <a href='{verification_url}'>Нажмите здесь, чтобы подтвердить</a>
           </body>
       </html>"""
    message = MessageSchema(
        subject="Подтверждение учетной записи",
        recipients=[email],
        body=template,
        subtype="html",
    )
    await fast_mail.send_message(message)
    print('Сообщение отправлено!')
