from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.enums import BotMode, Environment, LogLevel



class Settings(BaseSettings):
    environment: Environment = Environment.DEVELOPMENT
    bot_mode: BotMode = BotMode.POLLING
    log_level: LogLevel = LogLevel.INFO

    bot_token: str 
    root_user_id: int 

    database_url: str 

    webhook_url: str | None = None
    webhook_secret: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        return self.environment == Environment.TESTING

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    @property
    def use_webhook(self) -> bool:
        return self.bot_mode == BotMode.WEBHOOK


# create an cache pydantic settings object
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()