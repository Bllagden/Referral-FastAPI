from typing import Literal, TypeVar

# import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    # dotenv.load_dotenv()
    return cls()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        str_strip_whitespace=True,
        env_prefix="db_",
    )

    mode: Literal["DEV", "TEST", "PROD"]
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str

    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="auth_")
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    token_type: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="app_")
    allow_origins: list[str]


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="redis_")

    host: str
    port: str


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="smtp_")

    host: str
    port: str
    user: str
    password: str
