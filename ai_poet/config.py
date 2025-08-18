# ai_poet/config.py
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import pydantic
from packaging.version import parse as vparse

# -----------------------------------------------------------------------
# Handle Pydantic v1 vs v2 differences
# -----------------------------------------------------------------------
if vparse(pydantic.__version__).major >= 2:
    from pydantic_settings import BaseSettings
    from pydantic import Field, field_validator as validator
else:
    from pydantic import BaseSettings, Field, validator  # type: ignore

# Load .env file
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
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Validator — defined inline to avoid type resolution issues
    @validator("api_key", mode="before" if vparse(pydantic.__version__).major >= 2 else ...)
    def key_must_exist(cls, v: Optional[str]):
        if not v or not v.strip():
            raise ValueError("API_KEY missing. Add it to .env or export it.")
        return v.strip()

    class Config:
        env_file = dotenv_path if dotenv_path.exists() else None
        env_file_encoding = "utf-8"
        # For v2, extra settings
        model_config = {} if vparse(pydantic.__version__).major < 2 else {
            "extra": "allow",
            "env_file": env_file,
            "env_file_encoding": "utf-8",
        }

@lru_cache
def get_settings() -> Settings:
    return Settings()