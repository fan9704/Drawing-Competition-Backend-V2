"""Some vars"""
from os import environ
from dotenv import load_dotenv

load_dotenv()

APPLICATION_PORT = 8000

IS_TEST = bool(environ.get("API_TEST"))
SECRET_KEY = environ.get("SECRET_KEY")
API_ENDPOINT = environ.get("API_ENDPOINT", "http://localhost:8000")
GENERATE_DB_SCHEMA = environ.get("GENERATE_DB_SCHEMA", False)
ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

DRAWING_TEMPLATE_PATH = "src/utils/judge_dir/drawing_code_template.py"
MAIN_DRAWING_PATH = f"src/utils/judge_dir/main_drawing.py"

NGROK_AUTH_TOKEN = environ.get("NGROK_AUTH_TOKEN", "")
NGROK_EDGE = environ.get("NGROK_EDGE", "edge:edghts_")

REDIS_URL = environ.get("REDIS_URL")
