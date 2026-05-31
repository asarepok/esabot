from core.config import settings

def test_config_loaded():
    assert settings.bot_token
    assert settings.database_url