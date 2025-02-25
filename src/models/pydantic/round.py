import datetime
from typing import List

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.tortoise.round import Round as IRound
from src.models.pydantic.challenge import ChallengePydantic

RoundPydantic = pydantic_model_creator(IRound, name="Round")


class Round(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_valid: bool = Field(default=True,examples=[True])

    class Config:
        from_attributes = True


class RoundChallengeResponse(BaseModel):
    id: int = Field()
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_valid: bool = Field(default=True,examples=[True])
    challenge_list: List[ChallengePydantic]
