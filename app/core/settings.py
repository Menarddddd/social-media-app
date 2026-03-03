from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

    DATABASE_URL: SecretStr
    SECRET_KEY: SecretStr
    ALGORITHM: str
    EXPIRE_MINUTES: int
    EMAIL_USER: SecretStr
    EMAIL_PASS: SecretStr


settings = Settings()  # type: ignore
