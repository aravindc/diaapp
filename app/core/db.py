from dynaconf import settings
from pydantic import PostgresDsn

settings.setenv('dev')

DATABASE_URI = PostgresDsn.build(
        scheme="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        path=f"/{settings.POSTGRES_DB or ''}",    
)


DB_CONFIG = {
    "connections": {
        # "default": settings.DATABASE_URL.split('?')[0]
        "default": DATABASE_URI.split('?')[0]
    },
    "apps": {
        "models": {
            "models": settings.MODELS
        }
    }
}