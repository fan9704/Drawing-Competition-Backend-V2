from inspect import getmembers
from loguru import logger
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from tortoise.contrib.starlette import register_tortoise
from fastapi.staticfiles import StaticFiles
from src.configs import tortoise_config ,REDIS_URL
from src.utils.api.router import TypedAPIRouter
from fastapi.middleware.cors import CORSMiddleware


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)
    init_exceptions_handlers(app)
    # init_router(app)
    init_cors(app)
    init_redis(app)
    # 設定靜態文件的目錄（上傳檔案的存放位置）
    app.mount("/media", StaticFiles(directory="media"), name="media")


def init_cors(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:8000",
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_exceptions_handlers(app: FastAPI):
    from src.exceptions.handlers import tortoise_exception_handler
    from src.exceptions.handlers import BaseORMException

    app.add_exception_handler(BaseORMException, tortoise_exception_handler)

def init_redis(app:FastAPI):
    logger.info("Setting up Redis")
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    config = {
        "use_tz": True,
        "timezone": "Asia/Taipei",
        "connections": {
            "default": tortoise_config.db_url
        },
        "apps":{
            "models": {
                "models": ["src.models.tortoise"],
                'default_connection': 'default',
            }

        }
    }
    register_tortoise(
        app,
        config=config,
    )

def init_router(app:FastAPI):
    from src.routers import team
    app.include_router(team.router)
def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    :param app:
    :return:
    """

    from src import routers

    routers = [o[1] for o in getmembers(routers) if isinstance(o[1], TypedAPIRouter)]

    for router in routers:
        app.include_router(**router.dict())