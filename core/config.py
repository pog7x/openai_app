from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    AUTO_RELOAD: bool = False

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 5555

    PROJECT_NAME: str
    PROJECT_VERSION: str = "0.0.1"
    ROOT_URL: str = ""

    RATE_LIMIT: PositiveInt = 5
    RATE_LIMIT_LIFETIME: PositiveInt = 50

    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int

    OPENAI_API_KEY: str

    SECRET_USERNAME: str
    SECRET_PASSWORD: str

    DISABLE_DOCS: bool = False
    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
