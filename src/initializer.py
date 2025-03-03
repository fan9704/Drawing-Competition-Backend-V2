from inspect import getmembers

from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise
from fastapi.staticfiles import StaticFiles
from src.configs import tortoise_config, GENERATE_DB_SCHEMA, ALLOW_ORIGINS
from src.utils.api.router import TypedAPIRouter
from src.middlewares.language import LanguageMiddleware
from fastapi.middleware.cors import CORSMiddleware


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)
    init_exceptions_handlers(app)
    # 初始化 Middleware
    init_i18n(app)
    init_cors(app)
    # 設定靜態文件的目錄（上傳檔案的存放位置）
    app.mount("/media", StaticFiles(directory="media"), name="media")


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
        "apps": {
            "models": {
                "models": ["src.models.tortoise"],
                'default_connection': 'default',
            }

        }
    }
    register_tortoise(
        app,
        config=config,
        generate_schemas=GENERATE_DB_SCHEMA
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


def init_i18n(app: FastAPI):
    app.add_middleware(LanguageMiddleware)


def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
