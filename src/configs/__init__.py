"""Config of application"""
from src.configs.db import TortoiseSettings
from src.configs.openapi import OpenAPISettings
from src.configs.cfg import *
from src.configs.jwt import *

tortoise_config = TortoiseSettings.generate()
openapi_config = OpenAPISettings()