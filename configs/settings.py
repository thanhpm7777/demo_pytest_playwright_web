from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    USER_EMAIL: str
    USER_PASSWORD: str

    PW_BROWSER: str
    PW_HEADLESS: bool
    PW_TIMEOUT: int
    RECORD_VIDEO: bool

    # MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


# 👇 Đây là object đã được load sẵn, khi import vào test cứ dùng `settings.PW_TIMEOUT`
settings = get_settings()
