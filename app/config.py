from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Business Assistant"
    api_key: str = "change-me"
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    demo_mode: bool = True
    database_path: str = "data/agent_runs.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
