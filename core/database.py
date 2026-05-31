from tortoise import Tortoise
from core.config import settings



TORTOISE_ORM = {
    "connections": {
        "default": settings.database_url,
    },
    "apps": {
        "models": {
            "models": [
                "apps.school.models",
                "apps.users.models",
                "apps.materials.models",
                "apps.requests.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)

async def close_db() -> None:
    await Tortoise.close_connections()