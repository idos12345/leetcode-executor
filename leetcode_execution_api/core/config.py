from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    K8S_JOB_YAML_PATH: str
    REGISTRY_URL: str
    # KUBECONFIG: str

    class Config:
        env_file = ".env"

settings = Settings()