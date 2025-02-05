"""
Pydantic models.
"""
from pydantic import BaseModel
from src.models.pydantic.team import Team, TeamAuthRequest,TeamAuthResponse
from src.models.pydantic.round import Round,RoundChallengeResponse

class Item(BaseModel):
    id: int
    name: str