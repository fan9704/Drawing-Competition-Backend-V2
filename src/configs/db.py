"""Config of DB"""
from betterconf import betterconf, field, DotenvProvider

from src.configs.cfg import IS_TEST

DB_MODELS = ["src.models.tortoise"]
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://:memory:"

@betterconf(provider=DotenvProvider(auto_load=True))
class PostgresSettings:
    """Postgres env values"""

    postgres_user: str = field("POSTGRES_USER", default="postgres")
    postgres_password: str = field("POSTGRES_PASSWORD", default="postgres")
    postgres_db: str = field("POSTGRES_DB", default="mydb")
    postgres_port: str = field("POSTGRES_PORT", default="5432")
    postgres_host: str = field("POSTGRES_HOST", default="postgres")

@betterconf(provider=DotenvProvider(auto_load=True))
class RedisSettings:
    """Redis env values"""
    redis_host: str = field("REDIS_HOST", default="localhost")
    redis_port: str = field("REDIS_PORT", default="6379")
    redis_db: str = field("REDIS_DB", default="0")


class TortoiseSettings:
    """Tortoise-ORM settings"""

    def __init__(self, db_url: str, modules: dict, generate_schemas: bool):
        self.db_url = db_url
        self.modules = modules
        self.generate_schemas = generate_schemas

    @classmethod
    def generate(cls):
        """Generate Tortoise-ORM settings (with sqlite if tests)"""

        if IS_TEST:
            db_url = SQLITE_DB_URL
        else:
            postgres = PostgresSettings()
            db_url = POSTGRES_DB_URL.format(**vars(postgres))
            del postgres
        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True)