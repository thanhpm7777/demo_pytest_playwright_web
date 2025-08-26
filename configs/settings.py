from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    USER_EMAIL: str
    USER_PASSWORD: str

    PW_BROWSER: str = "chromium"
    PW_HEADLESS: bool = True
    PW_TIMEOUT: int = 10_000  # <== thêm default
    RECORD_VIDEO: bool = False

    # MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


# 👇 Đây là object đã được load sẵn, khi import vào test cứ dùng `settings.PW_TIMEOUT`
settings = get_settings()
