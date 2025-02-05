"""Some vars"""
from os import environ

IS_TEST = bool(environ.get("API_TEST"))
SECRET_KEY = environ.get("SECRET_KEY")
API_ENDPOINT = environ.get("API_ENDPOINT","http://localhost:8000")

DRAWING_TEMPLATE_PATH = "src/utils/judge_dir/drawing_code_template.py"
MAIN_DRAWING_PATH = f"src/utils/judge_dir/main_drawing.py"