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

class Role(StrEnum):
    STUDENT = "student"
    ADMIN = "admin"
    ROOT = "root"

class MaterialType(StrEnum):
    SLIDES = "slides"
    PAST_QUESTIONS = "past_questions"
    COURSE_OUTLINE = "course_outline"
    TIMETABLE = "timetable"
    BOOK = "book"
    OTHER = "other"