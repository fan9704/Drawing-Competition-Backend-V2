from datetime import timedelta, datetime
from typing import List, Optional, Any

from pydantic import BaseModel

from src.models.pydantic import Challenge
from src.models.pydantic.submission import SubmissionOneLayerPydantic

class StatisticTeamChallengeScoreResponseDTO(BaseModel):
    challenge: int
    team_id: int
    max_score: int
    submission: Optional[SubmissionOneLayerPydantic]

    class Config:
        from_attributes = True
class StatisticTeamChallengeSubmissionCountResponseDTO(BaseModel):
    challenge: int
    submission_count: int

class StatisticTeamRoundTotalScoreResponseDTO(BaseModel):
    round_id: int
    team_id: int
    total_score: int

class StatisticAllTeamSingleRoundTotalScoreResponseDTO(BaseModel):
    team_id: int
    team_name: str
    total_score: int
    score_list: List[int]

class StatisticAllTeamRoundTotalScoreResponseDTO(BaseModel):
    team_id: int
    team_name: str
    round_id_list: List[int]
    total_score_list: List[int]

class StatisticTop3TeamChallengeScoreResponseDTO(BaseModel):
    team: int
    team_name: str
    max_score: int
    fitness: Optional[float]
    execute_time: Optional[timedelta]
    word_count: Optional[int]

class StatisticOneLayerSubmissionResponseDTO(BaseModel):
    id: int
    team_id: int
    score: Optional[int] = 0
    code: Optional[str] = ""
    fitness: Optional[int] = 0
    word_count: Optional[int] = 0
    execution_time: Optional[int] = 0
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    status: Optional[str] = "doing"
    draw_image_url: Optional[str] = ""
    time: datetime = datetime.now()
    challenge_id: int
    round_id: int

class StatisticFeaturedSubmissionResponseDTO(BaseModel):
    challenge: Challenge
    submissions:List[StatisticOneLayerSubmissionResponseDTO] = []