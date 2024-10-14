from fastapi_mail import MessageSchema

from backend.src.users.schemas import UserCreate
from backend.src.core.config.email import fast_mail


class EmailSender:
    @staticmethod
    async def send(user_data: UserCreate):
        template = f"""<html>
            <body>
                <p>Для подтверждения вашей учетной записи, пройдите по следующей ссылке:</p>
                <a href='{1}'>Нажмите здесь, чтобы подтвердить</a>
            </body>
        </html>"""

        message = MessageSchema(
            subject="Подтверждение учетной записи",
            recipients=[user_data.email],
            body=template,
            subtype="html",
        )

        await fast_mail.send_message(message=message)
