import logging

import bcrypt

from src.exceptions import InvalidSalt

logger = logging.getLogger("main")


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: str | bytes) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()
    try:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password
        )
    except ValueError as ex:
        if "Invalid salt" in str(ex):
            raise InvalidSalt
