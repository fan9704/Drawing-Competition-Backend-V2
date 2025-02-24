from typing import Optional
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.tortoise import Team as ITeam

TeamPydanticWithoutToken = pydantic_model_creator(ITeam, exclude=("token",))
TeamPydantic = pydantic_model_creator(ITeam)


class Team(BaseModel):
    id: int
    name: str = Field(examples=["第1小隊"])


# 請求 Body 定義
class TeamAuthRequest(BaseModel):
    token: str = Field(examples=["ABCD"], min_length=4, max_length=4)


# 回應 Body 定義
class TeamAuthResponse(BaseModel):
    status: bool = Field(examples=[False])
    team: Optional[TeamPydanticWithoutToken]
    access_token: Optional[str]
