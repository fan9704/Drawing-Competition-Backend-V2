"""Config of application"""
from .db import TortoiseSettings
from .openapi import OpenAPISettings
from src.configs.cfg import *

tortoise_config = TortoiseSettings.generate()
openapi_config = OpenAPISettings()