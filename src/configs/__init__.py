"""Config of application"""
from .db import TortoiseSettings, RedisSettings
from .openapi import OpenAPISettings
from src.configs.cfg import *

tortoise_config = TortoiseSettings.generate()
openapi_config = OpenAPISettings()
redis_config = RedisSettings()