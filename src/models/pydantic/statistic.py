from typing import List, Optional, Any

from pydantic import BaseModel

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
    execute_time: Optional[float]
    word_count: Optional[int]