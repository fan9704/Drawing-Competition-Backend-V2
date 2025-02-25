from datetime import timedelta, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.models.pydantic.challenge import Challenge
from src.models.pydantic.submission import SubmissionOneLayerPydantic
from src.models.enums import StatusEnum


class StatisticTeamChallengeScoreResponseDTO(BaseModel):
    challenge: int = Field()
    team_id: int = Field()
    max_score: int = Field(default=0, examples=[0], gt=0)
    submission: Optional[SubmissionOneLayerPydantic]

    class Config:
        from_attributes = True


class StatisticTeamChallengeSubmissionCountResponseDTO(BaseModel):
    challenge: int = Field()
    submission_count: int = Field(default=0, examples=[1], ge=0)


class StatisticTeamRoundTotalScoreResponseDTO(BaseModel):
    round_id: int = Field()
    team_id: int = Field()
    total_score: int = Field(default=0, examples=[0], ge=0)


class StatisticAllTeamSingleRoundTotalScoreResponseDTO(BaseModel):
    team_id: int = Field()
    team_name: str = Field(examples=["第1小隊"])
    total_score: int = Field(default=0, examples=[0], ge=0)
    score_list: List[int]


class StatisticAllTeamRoundTotalScoreResponseDTO(BaseModel):
    team_id: int = Field()
    team_name: str = Field(examples=["第1小隊"])
    round_id_list: List[int]
    total_score_list: List[int]


class StatisticTop3TeamChallengeScoreResponseDTO(BaseModel):
    team: int = Field()
    team_name: str = Field(examples=["第1小隊"])
    max_score: int = Field(default=0, examples=[0], ge=0)
    fitness: Optional[float] = Field(default=0.0, examples=[21.3], ge=0.0, le=0.0)
    execute_time: Optional[timedelta]
    word_count: Optional[int] = Field(default=0, examples=[0], ge=0)


class StatisticOneLayerSubmissionResponseDTO(BaseModel):
    id: int = Field()
    team_id: int = Field()
    score: int = Field(default=0, examples=[0], ge=0, le=100)
    code: str = Field(default="")
    fitness: Optional[int] = Field(default=0, examples=[0], ge=0)
    word_count: Optional[int] = Field(default=0, examples=[0], ge=0)
    execution_time: Optional[int] = Field(default=0, examples=[0])
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    status: StatusEnum = Field(default=StatusEnum.doing, examples=[StatusEnum.todo])
    draw_image_url: Optional[str] = Field(default="images/default.png")
    time: datetime = Field(default=datetime.now())
    challenge_id: int = Field()
    round_id: int = Field()


class StatisticFeaturedSubmissionResponseDTO(BaseModel):
    challenge: Challenge
    submissions: List[StatisticOneLayerSubmissionResponseDTO] = []
