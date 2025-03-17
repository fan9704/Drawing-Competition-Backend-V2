from typing import List, Optional

from fastapi import APIRouter, Query, Path, Depends

from src.models.pydantic.statistic import StatisticTeamChallengeScoreResponseDTO, \
    StatisticTeamChallengeSubmissionCountResponseDTO, StatisticTeamRoundTotalScoreResponseDTO, \
    StatisticAllTeamSingleRoundTotalScoreResponseDTO, StatisticTop3TeamChallengeScoreResponseDTO, \
    StatisticAllTeamRoundTotalScoreResponseDTO, StatisticOneLayerSubmissionResponseDTO, \
    StatisticFeaturedSubmissionResponseDTO
from src.repositories import SubmissionRepository
from src.dependencies import get_submission_repository
from src.services.statistic import (
    find_all_highest_submission_by_team_id,
    count_team_all_count_submission,
    get_team_round_total_score,
    get_all_round_team_total_challenge_score,
    get_team_all_challenge_score,
    get_top3_challenge_score_by_team_id,
    find_all_challenge_featured_submission
)

router = APIRouter()


@router.get("/team/",
            summary="取得隊伍各挑戰最高成績",
            description="Get Highest Score in every challenge by team_id",
            response_model=List[StatisticTeamChallengeScoreResponseDTO],
            response_description="Team in every challenge highest score",
            )
async def get_team_challenge_highest_score(team_id: Optional[int] = Query(None),
                                           repository: SubmissionRepository = Depends(get_submission_repository)) -> \
        List[StatisticTeamChallengeScoreResponseDTO]:
    highest_scores = await find_all_highest_submission_by_team_id(team_id)
    return highest_scores


# TODO: Change Route
# /submission/ -> /count/
@router.get("/count/",
            summary="取得隊伍提交各挑戰次數",
            description="Get Submit count in every challenge by team_id",
            response_model=List[StatisticTeamChallengeSubmissionCountResponseDTO],
            response_description="Submit count in every challenge",
            )
async def get_team_challenge_submission_count(team_id: Optional[int] = Query(None),
                                              repository: SubmissionRepository = Depends(get_submission_repository)) -> \
        List[StatisticTeamChallengeSubmissionCountResponseDTO]:
    # TODO: Check Valid Team
    team_submission_count = await count_team_all_count_submission(team_id)
    return team_submission_count


@router.get("/round/{round_id}/team/",
            summary="取的隊伍該回合分數",
            description="Get round by round_id score by team_id",
            response_model=StatisticTeamRoundTotalScoreResponseDTO,
            response_description="Team Round Score")
async def get_team_round_total_score(round_id: int = Path(...), team_id: Optional[int] = Query(None),
                                     repository: SubmissionRepository = Depends(
                                         get_submission_repository)) -> StatisticTeamRoundTotalScoreResponseDTO:
    team_round_total_score = await get_team_round_total_score(team_id, round_id)
    return team_round_total_score


@router.get("/round/allTeam/",
            summary="取得所有回合所有隊伍成績",
            description="Get All Round All Team Score",
            response_model=List[StatisticAllTeamRoundTotalScoreResponseDTO],
            response_description="All Round Team Score"
            )
async def get_team_round_all_teams(repository: SubmissionRepository = Depends(get_submission_repository)) -> List[
    StatisticAllTeamRoundTotalScoreResponseDTO]:
    all_round_team_total_challenge_score = await get_all_round_team_total_challenge_score()
    return all_round_team_total_challenge_score


@router.get("/round/{round_id}/allTeam/",
            summary="取得該回合所有隊伍成績",
            description="Get Round by round_id All Team Score",
            response_model=List[StatisticAllTeamSingleRoundTotalScoreResponseDTO],
            response_description="Round Team Score")
async def get_all_team_single_round_total_score(round_id: int = Path(...), repository: SubmissionRepository = Depends(
    get_submission_repository)) -> List[StatisticAllTeamSingleRoundTotalScoreResponseDTO]:
    all_team_total_score = await get_team_all_challenge_score(round_id)
    return all_team_total_score


@router.get("/challenge/{challenge_id}/top3Team/",
            summary="取得該挑戰前三高隊伍成績",
            description="Get Challenge Top 3 Team Score",
            response_model=List[StatisticTop3TeamChallengeScoreResponseDTO],
            response_description="Challenge Top 3 Team Score")
async def get_top3_team_challenge_score(challenge_id: int = Path(...),
                                        repository: SubmissionRepository = Depends(get_submission_repository)) -> List[
    StatisticTop3TeamChallengeScoreResponseDTO]:
    top3_team_challenge_score = await get_top3_challenge_score_by_team_id(challenge_id)
    return top3_team_challenge_score


@router.get("/challenge/{challenge_id}/team/{team_id}/success/",
            summary="取得該挑戰該隊伍所有成功提交",
            description="Get Challenge Team Challenge Success Submission",
            response_model=List[StatisticOneLayerSubmissionResponseDTO],
            response_description="Challenge Team Challenge Success Submission")
async def get_all_success_submission_by_challenge_id_and_team_id(team_id: int, challenge_id: int,
                                                                 repository: SubmissionRepository = Depends(
                                                                     get_submission_repository)):
    all_success_submission = await repository.find_all_success_submission_by_challenge_id_and_team_id(team_id,
                                                                                                      challenge_id)
    return all_success_submission


@router.get("/challenge/{challenge_id}/allTeam/success/",
            summary="取得該挑戰所有隊伍成功提交",
            description="Get Challenge ID All Team Success Submission",
            response_model=List[StatisticOneLayerSubmissionResponseDTO],
            response_description="Challenge All Team Success Submission")
async def get_all_team_success_submission_challenge_id(challenge_id: int, repository: SubmissionRepository = Depends(
    get_submission_repository)):
    all_team_success_submission = await repository.find_all_team_success_submission_challenge_id(challenge_id)
    return all_team_success_submission


@router.get("/challenge/all/featured/allTeam/success/",
            summary="取得所有挑戰提交精選圖片",
            description="Get Challenge All TeamSubmission Featured Pictures",
            response_model=List[StatisticFeaturedSubmissionResponseDTO],
            response_description="Challenge All Team Submission Featured Pictures")
async def get_all_challenge_featured_submission(repository: SubmissionRepository = Depends(get_submission_repository)):
    all_challenge_featured_submission = await find_all_challenge_featured_submission()
    return all_challenge_featured_submission
