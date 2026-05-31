import pytest_asyncio
from tortoise import Tortoise



TEST_TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:",
    },
    "apps": {
        "models": {
            "models": [
                "apps.school.models",
                "apps.users.models",
                "apps.materials.models",
                "apps.requests.models",
            ],
            "default_connection": "default",
        },
    },
}

# initialize test database for each test
@pytest_asyncio.fixture(scope="function", autouse=True)
async def db():
    await Tortoise.init(config=TEST_TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()