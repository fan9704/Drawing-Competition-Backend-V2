from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.tortoise import Team

TeamGeneralSerializer = pydantic_model_creator(Team, name="TeamGeneral", include=("id", "name"))
