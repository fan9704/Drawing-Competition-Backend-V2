"""Some vars"""
from os import environ

IS_TEST = bool(environ.get("API_TEST"))
SECRET_KEY = environ.get("SECRET_KEY")