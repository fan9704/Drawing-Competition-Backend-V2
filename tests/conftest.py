import asyncio
import os
from asyncio import AbstractEventLoop
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
from testcontainers.postgres import PostgresContainer
from tortoise import Tortoise
from tortoise.contrib.test import getDBConfig

from tests.common import setup_test_logger

load_dotenv()

# DB Config
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_TEST_DB")
POSTGRES_DB_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DB_MODELS = ["src.models.tortoise"]

os.environ["TESTING"] = "1"
os.environ["POSTGRES_USER"] = POSTGRES_USER
os.environ["POSTGRES_PASSWORD"] = POSTGRES_PASSWORD
os.environ["POSTGRES_HOST"] = POSTGRES_HOST
os.environ["POSTGRES_PORT"] = POSTGRES_PORT
os.environ["POSTGRES_DB"] = POSTGRES_DB


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
# @pytest.fixture(scope="module")
def postgres_container():
    """使用 Testcontainers 啟動 PostgreSQL"""
    container = PostgresContainer("postgres:15")
    container.start()
    yield container  # 提供給測試使用
    container.stop()  # 測試結束後停止容器


@pytest.fixture(scope="session")
# @pytest.fixture(scope="module")
def in_memory_db(request, event_loop, postgres_container):
    config = getDBConfig(
        app_label="models",
        modules=["src.models.tortoise"],
    )
    config["connections"]["default"] = (postgres_container.get_connection_url()
                                        .replace("postgresql+psycopg2://", "asyncpg://"))
    print(postgres_container.get_connection_url())

    async def init_db():
        await Tortoise.init(config)
        await Tortoise.generate_schemas()

    event_loop.run_until_complete(init_db())

    def finalizer():
        async def cleanup():
            await Tortoise.close_connections()  # 先關閉連線
            # await Tortoise._drop_databases()  # 再刪除資料庫

        event_loop.run_until_complete(cleanup())

    request.addfinalizer(finalizer)
    # request.addfinalizer(lambda: event_loop.run_until_complete(Tortoise._drop_databases()))

@pytest.fixture()
def logger(request):
    """動態產生 Logger，名稱與當前測試函式對應"""
    test_name = request.node.name
    logger = setup_test_logger(test_name)
    return logger

@pytest_asyncio.fixture(scope="module")
async def http_client() -> AsyncClient:
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def dependencies(request):
    args = request.config

    if args.getoption("prod"):
        load_dotenv(".env.prod")
    elif args.getoption("test"):
        load_dotenv(".env.test")
    elif args.getoption("dev"):
        load_dotenv(".env.dev")
    else:
        load_dotenv()

    if args.getoption("sync"):
        os.environ["RUN_MODE"] = "SYNC"
    else:
        os.environ["RUN_MODE"] = "ASYNC"

    os.environ["DB_TYPE"] = args.getoption("db")
    print("DB_TYPE", os.getenv("DB_TYPE"))


def pytest_addoption(parser):
    parser.addoption("--prod", action="store_true", help="Run the server in production mode.")
    parser.addoption("--test", action="store_true", help="Run the server in test mode.")
    parser.addoption("--dev", action="store_true", help="Run the server in development mode.")
    parser.addoption("--sync", action="store_true", help="Run the server in Sync mode.")
    parser.addoption("--db", help="Run the server in database type.", choices=["mysql", "postgresql"],
                     default="postgresql")
