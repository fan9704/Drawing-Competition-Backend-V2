from inspect import getmembers

from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise

from src.configs import tortoise_config
from src.utils.api.router import TypedAPIRouter


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)
    init_exceptions_handlers(app)
    # init_router(app)


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
    register_tortoise(
        app,
        db_url=tortoise_config.db_url,
        generate_schemas=tortoise_config.generate_schemas,
        modules=tortoise_config.modules,
    )

def init_router(app:FastAPI):
    from src.routers import items,team
    app.include_router(items.router)
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