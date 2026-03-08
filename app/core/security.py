import jwt
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta

from app.core.settings import settings


password_hash = PasswordHash.recommended()


def hash_password(plain_pwd: str) -> str:
    return password_hash.hash(plain_pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return password_hash.verify(plain_pwd, hashed_pwd)


def create_access_token(sub: dict):
    to_encode = sub.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_EXPIRE_MINUTES
    )

    access_token = jwt.encode(
        to_encode, settings.ACCESS_SECRET_KEY.get_secret_value(), settings.ALGORITHM
    )

    return access_token
