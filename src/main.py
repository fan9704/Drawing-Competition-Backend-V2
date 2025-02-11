"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

logging.basicConfig(level="DEBUG")
APPLICATION_PORT = 8000

from src.configs import openapi_config
from src.initializer import init, init_redis_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)
logger.info("Starting application initialization...")
init(app)
logger.success("Successfully initialized!")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT, reload=True)
