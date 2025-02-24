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
    id: int
    code: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    score: conint(ge=0, le=100) = 0  # 限制分數在 0 到 100 之間
    fitness: conint(ge=0, le=100) = 0  # 限制吻合度在 0 到 100 之間
    word_count: int = 0
    execute_time: Optional[timedelta] = None
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    team: TeamPydantic  # 假設這是 team 的 ID (ForeignKey)
    time: datetime = Field(default=datetime.now())
    challenge: ChallengePydantic  # 假設這是 challenge 的 ID (ForeignKey)
    round: RoundPydantic  # 假設這是 round 的 ID (ForeignKey)
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])

    class Config:
        from_attributes = True  # 允許從 ORM 對象進行轉換


class SubmissionOneLayer(BaseModel):
    id: int
    code: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    score: conint(ge=0, le=100) = 0  # 限制分數在 0 到 100 之間
    fitness: conint(ge=0, le=100) = 0  # 限制吻合度在 0 到 100 之間
    word_count: int = 0
    execute_time: Optional[timedelta] = None
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    team: int
    time: datetime = Field(default=datetime.now())
    challenge: int
    round: int
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])


class SubmissionStoreJudgeRequest(BaseModel):
    score: Optional[int] = Field(examples=[0], gt=0)
    fitness: Optional[int] = Field(examples=[0], gt=0)
    word_count: Optional[int] = Field(examples=[0], gt=0)
    execution_time: Optional[int] = Field(examples=[0], gt=0)
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])


class SubmissionStoreJudgeResponse(BaseModel):
    id: int
    team_id: int
    score: Optional[int] = Field(examples=[0], gt=0)
    code: str = Field(default="")
    fitness: Optional[int] = Field(examples=[0], gt=0)
    word_count: Optional[int] = Field(examples=[0], gt=0)
    execution_time: Optional[int] = Field(examples=[0], gt=0)
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    time: datetime = Field(default=datetime.now())
    challenge_id: int
    round_id: int


class SubmissionSubmitCodeRequest(BaseModel):
    code: str = Field(default="")
    team: int
    challenge: int

    class Config:
        from_attributes = True


class SubmissionSubmitCodeResponse(BaseModel):
    challenge: int
    code: str = Field(default="")
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    round: int
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    team: int
    time: datetime = Field(default=datetime.now())


class SubmissionTeamRecordResponse(BaseModel):
    team_id: int
    stderr: str = Field(default="")
    challenge_id: int
    round_id: int
    status: StatusEnum = Field(examples=[StatusEnum.todo])
    code: str = Field(default="")
    execute_time: Optional[timedelta] = Field(examples=[0], gt=0)
    score: Optional[conint(ge=0, le=100)] = 0
    stdout: str = Field(default="")
    draw_image_url: Optional[str] = Field(default="/images/default.png", examples=["/images/default.png"])
    id: int
    fitness: int = Field(examples=[0], gt=0)
    time: datetime = Field(default=datetime.now())
    word_count: int = Field(examples=[0], gt=0)
