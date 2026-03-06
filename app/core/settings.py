from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: SecretStr
    DATABASE_USERNAME: SecretStr
    DATABASE_PASSWORD: SecretStr

    ACCESS_SECRET_KEY: SecretStr
    ACCESS_EXPIRE_MINUTES: int

    REFRESH_SECRET_KEY: SecretStr
    REFRESH_EXPIRE_DAYS: int

    ALGORITHM: str


settings = Settings()  # type: ignore LOADED FROM ENV FILE
