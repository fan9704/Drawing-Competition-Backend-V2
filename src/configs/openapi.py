"""OpenAPI-schema"""
from betterconf import betterconf,field

OPENAPI_API_NAME = "Drawing Competition API Sever"
OPENAPI_API_VERSION = "0.0.1 beta"
OPENAPI_API_DESCRIPTION = "API for Submit"

@betterconf
class OpenAPISettings:
    name: str = field("name", default=OPENAPI_API_NAME)
    version: str = field("version", default=OPENAPI_API_VERSION)
    description: str = field("description", default=OPENAPI_API_DESCRIPTION)