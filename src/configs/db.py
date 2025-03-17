"""Config of DB"""
import os

from src.configs.cfg import IS_TEST

# DB Config
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")
POSTGRES_DB_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DB_MODELS = ["src.models.tortoise"]
SQLITE_DB_URL = "sqlite://:memory:"


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
            db_url = POSTGRES_DB_URL
        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True)
