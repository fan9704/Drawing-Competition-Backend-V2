"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
# from loguru import logger
from src.configs import NGROK_EDGE, NGROK_AUTH_TOKEN
from src.utils.logger import logger
# import logging
import ngrok
import uvicorn

# logging.basicConfig(level="DEBUG")
APPLICATION_PORT = 8000

from src.configs import openapi_config
from src.initializer import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info("Setting up Ngrok Tunnel")
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    ngrok.forward(
        addr=APPLICATION_PORT,
        labels=NGROK_EDGE,
        proto="labeled",
    )
    yield
    # logger.info("Tearing Down Ngrok Tunnel")
    ngrok.disconnect()


app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)
logger.info("Starting application initialization...")
init(app)
logger.success("Successfully initialized!")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT,log_config=None, reload=True)
