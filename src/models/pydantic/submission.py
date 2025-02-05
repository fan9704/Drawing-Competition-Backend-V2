from pydantic import BaseModel, validator, conint
from typing import Optional
from datetime import datetime, timedelta

from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.tortoise.submission import Submission as ISubmission
from src.models.pydantic import RoundPydantic
from src.models.pydantic.team import TeamPydantic
from src.models.pydantic.challenge import ChallengePydantic

SubmissionPydantic = pydantic_model_creator(ISubmission, name="Submission")

class Submission(BaseModel):
    id: int
    code: Optional[str] = ""
    status: Optional[str] = "todo"
    score: conint(ge=0, le=100) = 0  # 限制分數在 0 到 100 之間
    fitness: conint(ge=0, le=100) = 0  # 限制吻合度在 0 到 100 之間
    word_count: int = 0
    execute_time: Optional[timedelta] = None
    stdout: Optional[str] = ""
    stderr: Optional[str]= ""
    team: TeamPydantic  # 假設這是 team 的 ID (ForeignKey)
    time: datetime = datetime.now()
    challenge: ChallengePydantic  # 假設這是 challenge 的 ID (ForeignKey)
    round: RoundPydantic  # 假設這是 round 的 ID (ForeignKey)
    draw_image_url: Optional[str] = ""

    @validator('status')
    def validate_status(cls, v):
        status_options = ["todo", "doing", "fail", "success"]
        if v not in status_options:
            raise ValueError(f"Status must be one of {status_options}")
        return v

    class Config:
        orm_mode = True  # 允許從 ORM 對象進行轉換

class SubmissionStoreJudgeRequest(BaseModel):
    score: Optional[int] = None
    fitness: Optional[int] = None
    word_count: Optional[int] = None
    execution_time: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    status: Optional[str] = None

class SubmissionSubmitCodeRequest(BaseModel):
    code: str
    team:  int
    challenge: int

    class Config:
        orm_mode = True  # 支援 ORM 映射

class SubmissionSubmitCodeResponse(BaseModel):
    challenge:int
    code: str
    draw_image_url: Optional[str] = None
    round: int
    status: str
    team:int
    time: datetime

class SubmissionTeamRecordResponse(BaseModel):
    team_id:int
    stderr: Optional[str] = ""
    challenge_id:int
    round_id: int
    status: str
    code: str
    execute_time: Optional[timedelta] = None
    score: Optional[conint(ge=0, le=100)] = 0
    stdout: Optional[str] = ""
    draw_image_url: Optional[str] = None
    id: int
    fitness: Optional[float] = 0
    time: datetime = datetime.now()
    word_count:int =0