from inspect import getmembers
from typing import AsyncIterator
from fastapi import FastAPI
from redis import Redis
from tortoise.contrib.starlette import register_tortoise
from fastapi.staticfiles import StaticFiles
from src.configs import tortoise_config,redis_config
from src.utils.api.router import TypedAPIRouter
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis

def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)
    init_exceptions_handlers(app)
    init_cors(app)
    init_redis_pool()
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
def init_redis_pool() -> Redis:
    pool = redis.ConnectionPool(host=redis_config.redis_host, port=redis_config.redis_port, db=redis_config.redis_db)
    return redis.Redis(connection_pool=pool)

def init_exceptions_handlers(app: FastAPI):
    from src.exceptions.handlers import tortoise_exception_handler
    from src.exceptions.handlers import BaseORMException

    app.add_exception_handler(BaseORMException, tortoise_exception_handler)



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