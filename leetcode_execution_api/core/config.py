from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    REGISTRY_URL: str
    NAMESPACE: str
    SWR_LOGIN_U: str
    SWR_LOGIN_P: str

    class Config:
        env_file = ".env"


settings = Settings()
