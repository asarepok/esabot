from enum import StrEnum

class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class BotMode(StrEnum):
    POLLING = "polling"
    WEBHOOK = "webhook"

class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
