from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.tortoise import Team as ITeam

TeamPydanticWithoutToken = pydantic_model_creator(ITeam, exclude=("token",))

class Team(BaseModel):
    id: int
    name: str

# 請求 Body 定義
class TeamAuthRequest(BaseModel):
    token: str

# 回應 Body 定義
class TeamAuthResponse(BaseModel):
    status: bool
    team: Optional[TeamPydanticWithoutToken]
    access_token: Optional[str]