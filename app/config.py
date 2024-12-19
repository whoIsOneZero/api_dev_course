# from pydantic import BaseSettings
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Performs validation to see if all these env variables have been set
    """

    database_hostname: Optional[str] = None
    database_port: Optional[str] = None
    database_password: Optional[str] = None
    database_name: Optional[str] = None
    database_username: Optional[str] = None
    database_url: Optional[str] = None
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
