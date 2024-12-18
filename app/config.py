# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Performs validation to see if all these env variables have been set
    """

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    # database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
