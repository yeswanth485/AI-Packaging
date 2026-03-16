from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "dev"

    # Required in production; for local imports we can keep them empty/defaults
    database_url: str = ""

    jwt_secret_key: str = "CHANGE_ME_DEV_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    ml_model_path: str = "packaging_model.pkl"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-arg]

