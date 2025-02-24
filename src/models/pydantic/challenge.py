from src.models.enums import StatusEnum,DifficultyEnum
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.tortoise import Challenge as IChallenge

ChallengePydantic = pydantic_model_creator(IChallenge, name="Challenge")
ChallengeWithOutRelationPydantic = pydantic_model_creator(IChallenge, exclude=("team", "challenge"),
                                                          name="ChallengeWithoutRelation")


class Challenge(BaseModel):
    id: int = Field()
    title: str = Field(examples=["題目名稱"])
    description: str = Field(examples=["題目描述"])
    image_url: str = Field(default="/images/default.png")
    difficulty: DifficultyEnum = Field(examples=[DifficultyEnum.easy])
    round_id: int
    is_valid: bool = Field(examples=[True])


class ChallengeTeamSubmissionResponse(BaseModel):
    id: int
    title: str = Field(examples=["題目名稱"])
    description: str = Field(examples=["題目描述"])
    round_id: int
    is_valid: bool = Field(examples=[True])
    difficulty: DifficultyEnum = Field(examples=[DifficultyEnum.easy])
    status: StatusEnum = Field(examples=[StatusEnum.todo])
