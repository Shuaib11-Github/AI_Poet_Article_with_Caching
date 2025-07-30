# ai_poet/config.py
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import pydantic
from packaging.version import parse as vparse

# ---------------------------------------------------------------------------
# Pydantic v1  → BaseSettings & validator live in pydantic
# Pydantic v2  → BaseSettings lives in pydantic_settings, validator renamed
# ---------------------------------------------------------------------------
if vparse(pydantic.__version__).major >= 2:
    from pydantic_settings import BaseSettings          # type: ignore
    from pydantic import Field, field_validator as _validator
else:
    from pydantic import BaseSettings, Field, validator as _validator  # type: ignore

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    """Central configuration object (env-driven)."""

    api_key: str
    base_url: str = "https://api.euron.one/api/v1/euri/chat/completions"
    default_model: str = "gpt-4.1-nano"
    max_tokens: int = 1000
    temperature: float = 0.7
    enable_cache: bool = True
    # cache_path: Path = Path.home() / ".ai_poet_cache.sqlite"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    @_validator("api_key", mode="before")   # v1 ignores `mode`
    def key_must_exist(cls, v: Optional[str]):  # noqa: N805
        if not v:
            raise ValueError(
                "API_KEY missing. Add it to .env or export it."
            )
        return v

    class Config:
        env_file = dotenv_path
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()      # singleton