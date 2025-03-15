from pydantic import BaseModel, conint, Field
from typing import Optional
from datetime import datetime, timedelta

from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.enums import StatusEnum
from src.models.tortoise.submission import Submission as ISubmission
from src.models.pydantic import RoundPydantic
from src.models.pydantic.team import TeamPydantic
from src.models.pydantic.challenge import ChallengePydantic

SubmissionPydantic = pydantic_model_creator(ISubmission, name="Submission")
SubmissionOneLayerPydantic = pydantic_model_creator(ISubmission, exclude=("team", "challenge", "round"),
                                                    name="Submission")


class Submission(BaseModel):
    id: int = Field()
    code: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    fitness: int = Field(default=0, examples=[0], ge=0, le=100)
    word_count: int = Field(default=0, examples=[0], ge=0)
    execute_time: Optional[timedelta] = None
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    team: TeamPydantic = Field()
    time: datetime = Field(default=datetime.now())
    challenge: ChallengePydantic
    round: RoundPydantic
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])

    class Config:
        from_attributes = True  # 允許從 ORM 對象進行轉換


class SubmissionOneLayer(BaseModel):
    id: int = Field()
    code: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    fitness: int = Field(default=0, examples=[0], ge=0, le=100)
    word_count: int = Field(default=0, examples=[0], ge=0)
    execute_time: Optional[timedelta] = None
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    team: int = Field()
    time: datetime = Field(default=datetime.now())
    challenge: int = Field()
    round: int = Field()
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])


class SubmissionStoreJudgeRequest(BaseModel):
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    fitness: int = Field(default=0, examples=[0], ge=0, le=100)
    word_count: int = Field(default=0, examples=[0], ge=0)
    execute_time: Optional[int] = Field(examples=[0], ge=0)
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])


class SubmissionStoreJudgeResponse(BaseModel):
    id: int = Field()
    team_id: int = Field()
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    code: str = Field(default="")
    fitness: int = Field(default=0, examples=[0], ge=0, le=100)
    word_count: int = Field(default=0, examples=[0], ge=0)
    execute_time: Optional[timedelta] = Field(examples=[0], ge=0)
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    status: StatusEnum = Field(default=StatusEnum.doing, examples=[StatusEnum.todo])
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    time: datetime = Field(default=datetime.now())
    challenge_id: int = Field()
    round_id: int = Field()


class SubmissionSubmitCodeRequest(BaseModel):
    code: str = Field(default="")
    team: int = Field()
    challenge: int = Field()

    class Config:
        from_attributes = True


class SubmissionSubmitCodeResponse(BaseModel):
    challenge: int = Field()
    code: str = Field(default="")
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    round: int = Field()
    status: StatusEnum = Field(default=StatusEnum.doing, examples=[StatusEnum.todo])
    team: int = Field()
    time: datetime = Field(default=datetime.now())


class SubmissionTeamRecordResponse(BaseModel):
    id: int = Field()
    team_id: int = Field()
    stderr: str = Field(default="")
    challenge_id: int = Field()
    round_id: int = Field()
    status: StatusEnum = Field(default=StatusEnum.todo, examples=[StatusEnum.todo])
    code: str = Field(default="")
    execute_time: Optional[timedelta] = Field(examples=[0], ge=0)
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    stdout: str = Field(default="")
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    fitness: int = Field(default=0, examples=[0], ge=0, le=100)
    time: datetime = Field(default=datetime.now())
    word_count: int = Field(default=0, examples=[0], ge=0)
