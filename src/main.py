"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from src.configs import openapi_config, APPLICATION_PORT
from src.initializer import init
import logging
import uvicorn

logging.basicConfig(level="DEBUG")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Setting up")
    yield


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
