from typing import List, Optional

from fastapi import APIRouter, Query, Path, HTTPException, Depends

from src.models.pydantic.statistic import StatisticTeamChallengeScoreResponseDTO, \
    StatisticTeamChallengeSubmissionCountResponseDTO, StatisticTeamRoundTotalScoreResponseDTO, \
    StatisticAllTeamSingleRoundTotalScoreResponseDTO, StatisticTop3TeamChallengeScoreResponseDTO, \
    StatisticAllTeamRoundTotalScoreResponseDTO
from src.models.tortoise import Challenge as IChallenge
from src.models.tortoise import Round as IRound
from src.models.tortoise import Submission as ISubmission
from src.models.tortoise import Team as ITeam
from src.repositories import SubmissionRepository, ChallengeRepository, TeamRepository, RoundRepository

router = APIRouter()

# Repository 依賴
def get_submission_repository() -> SubmissionRepository:
    return SubmissionRepository(ISubmission)

@router.get("/team/",
            response_model=List[StatisticTeamChallengeScoreResponseDTO]
            )
async def get_team_challenge_highest_score(team_id: Optional[int] = Query(None),repository:SubmissionRepository = Depends(get_submission_repository)) -> List[StatisticTeamChallengeScoreResponseDTO]:
    highest_scores = await repository.find_all_highest_submission_by_team_id(team_id)
    return highest_scores

# TODO: Change Route
# /submission/ -> /count/
@router.get("/count/", response_model=List[StatisticTeamChallengeSubmissionCountResponseDTO])
async def get_team_challenge_submission_count(team_id: Optional[int] = Query(None),repository:SubmissionRepository = Depends(get_submission_repository)) -> List[StatisticTeamChallengeSubmissionCountResponseDTO]:
    # TODO: Check Valid Team
    team_submission_count = await repository.count_team_all_count_submission(team_id)
    return team_submission_count

@router.get("/round/{round_id}/team/", response_model=StatisticTeamRoundTotalScoreResponseDTO)
async def get_team_round_total_score(round_id: int = Path(...), team_id: Optional[int] = Query(None),repository:SubmissionRepository = Depends(get_submission_repository)) -> StatisticTeamRoundTotalScoreResponseDTO:
    team_round_total_score = await repository.get_team_round_total_score(team_id, round_id)
    return team_round_total_score

@router.get("/round/allTeam/",response_model=List[StatisticAllTeamRoundTotalScoreResponseDTO])
async def get_team_round_all_teams(repository:SubmissionRepository = Depends(get_submission_repository)) -> List[StatisticAllTeamRoundTotalScoreResponseDTO]:
    all_round_team_total_challenge_score = await repository.get_all_round_team_total_challenge_score()
    return all_round_team_total_challenge_score

@router.get("/round/{round_id}/allTeam/", response_model=List[StatisticAllTeamSingleRoundTotalScoreResponseDTO])
async def get_all_team_single_round_total_score(round_id: int = Path(...),repository:SubmissionRepository = Depends(get_submission_repository))->List[StatisticAllTeamSingleRoundTotalScoreResponseDTO]:
    # if not round_instance:
    #     raise HTTPException(status_code=404, detail="Round not found")
    all_team_total_score = await repository.get_team_all_challenge_score(round_id)
    return all_team_total_score


@router.get("/challenge/{challenge_id}/top3Team/", response_model=List[StatisticTop3TeamChallengeScoreResponseDTO])
async def get_top3_team_challenge_score(challenge_id: int = Path(...),repository:SubmissionRepository = Depends(get_submission_repository))->List[StatisticTop3TeamChallengeScoreResponseDTO]:
    top3_team_challenge_score = await repository.get_top3_challenge_score_by_team_id(challenge_id)
    return top3_team_challenge_score

@router.get("/challenge/{challenge_id}/team/{team_id}/success/")
async def get_all_success_submission_by_challenge_id_and_team_id(team_id: int, challenge_id: int,repository:SubmissionRepository = Depends(get_submission_repository)):
    all_success_submission = await repository.find_all_success_submission_by_challenge_id_and_team_id(team_id, challenge_id)
    return all_success_submission

@router.get("/challenge/{challenge_id}/allTeam/success/")
async def get_all_team_success_submission_challenge_id(challenge_id: int,repository:SubmissionRepository = Depends(get_submission_repository)):
    all_team_success_submission = await repository.find_all_team_success_submission_challenge_id(challenge_id)
    return all_team_success_submission

@router.get("/challenge/all/featured/allTeam/success/")
async def get_all_challenge_featured_submission(repository:SubmissionRepository = Depends(get_submission_repository)):
    all_challenge_featured_submission = await repository.find_all_challenge_featured_submission()
    return all_challenge_featured_submission