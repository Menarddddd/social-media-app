import jwt
import hmac
import hashlib
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


def get_hashed_token(secret: str, token: str) -> str:
    return hmac.new(secret.encode(), token.encode(), hashlib.sha256).hexdigest()


def create_refresh_token(sub: dict):
    to_encode = sub.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_EXPIRE_DAYS
    )

    refresh_token = jwt.encode(
        to_encode, settings.REFRESH_SECRET_KEY.get_secret_value(), settings.ALGORITHM
    )

    hashed_token = get_hashed_token(
        settings.REFRESH_SECRET_KEY.get_secret_value(), refresh_token
    )

    # save hashed_token

    return refresh_token
