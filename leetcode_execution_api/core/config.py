from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    REGISTRY_URL: str
    REGISTRY_AUTH_NEEDED: bool = False
    NAMESPACE: str
    SWR_LOGIN_U: Optional[str] = None
    SWR_LOGIN_P: Optional[str] = None


settings = Settings()
