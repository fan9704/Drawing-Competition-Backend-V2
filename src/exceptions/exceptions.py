"""API Exceptions"""
from fastapi.exceptions import HTTPException
from starlette import status


class NotAuthenticated(HTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})

class CredentialsDataWrong(NotAuthenticated):
    DETAIL = "Could not validate credentials"