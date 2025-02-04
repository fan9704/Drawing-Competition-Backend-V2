"""
Pydantic models.
"""
from pydantic import BaseModel
from src.models.pydantic.team import Team

class Item(BaseModel):
    id: int
    name: str