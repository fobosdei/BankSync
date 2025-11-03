import os
from functools import lru_cache
from dotenv import load_dotenv


# Ensure .env is loaded when running via `uvicorn backend.app:app`
_CURRENT_DIR = os.path.dirname(__file__)
_ENV_PATH = os.path.abspath(os.path.join(_CURRENT_DIR, "..", ".env"))
load_dotenv(_ENV_PATH)


class Settings:
    app_name: str = "FastAPI Vue3 OAuth2"
    author: str = "Jason Liu"

    # Database
    database_url: str = os.getenv("DATABASE_URL", "")

    # Auth settings with sane defaults to prevent crashes if env is missing
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET", "dev-access-secret")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "180"))

    refresh_token_secret: str = os.getenv("REFRESH_TOKEN_SECRET", "dev-refresh-secret")
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "4320"))


@lru_cache()
def get_settings():
    return Settings()
