from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.utils.i18n import _
from src.models.pydantic import ChallengeWithOutRelationPydantic
from src.models.tortoise import Challenge as IChallenge
from src.models.pydantic.challenge import Challenge, ChallengeTeamSubmissionResponse
from src.repositories import ChallengeRepository, SubmissionRepository

router = APIRouter()


# Repository 依賴
def get_challenge_repository() -> ChallengeRepository:
    return ChallengeRepository()


def get_submission_repository() -> SubmissionRepository:
    return SubmissionRepository()


# 取得所有挑戰
@router.get("/",
            summary="取得所有 Challenge",
            description="Get All Challenge",
            response_model=List[ChallengeWithOutRelationPydantic],
            response_description="All Challenge"
            )
async def get_all_challenges(repository: ChallengeRepository = Depends(get_challenge_repository)):
    return await ChallengeWithOutRelationPydantic.from_queryset(repository.find_all())


# 取得單一挑戰 (根據 ID)
@router.get("/{pk}",
            summary="取得該 Challenge 透過 ID",
            description="Get Challenge by ID",
            response_model=Challenge,
            response_description="Challenge")
async def get_challenge_by_id(
        pk: int,
        repository: ChallengeRepository = Depends(get_challenge_repository)
) -> Challenge:
    challenge = await repository.find_by_id_with_round(pk=pk)
    if challenge:
        return challenge
    raise HTTPException(status_code=400, detail=_("Challenge is not valid"))


# 根據 team_id 列出挑戰
# TODO: Change Frontend Route
@router.get("/team/{team_id}",
            summary="Challenge Team 提交狀態",
            description="Get Challenge Submission Status Team by ID",
            response_model=List[ChallengeTeamSubmissionResponse],
            response_description="Team Challenge Submission Status")
async def list_challenges_by_team(
        team_id: int = None,
        repository: ChallengeRepository = Depends(get_challenge_repository),
        submission_repository: SubmissionRepository = Depends(get_submission_repository),
) -> List[ChallengeTeamSubmissionResponse]:
    if team_id is None:
        raise HTTPException(status_code=400, detail=_("team_id is required"))

    challenges: List[IChallenge] = await repository.filter()
    challenge_status_list = []
    for challenge in challenges:
        challenge_status = await submission_repository.filter_submission_by_challenge(team_id, challenge)
        c_status = "todo"
        if challenge_status is not None:
            c_status = challenge_status.status
        challenge_status_list.append(c_status)

    team_challenges = [
        ChallengeTeamSubmissionResponse(
            id=challenge.id,
            title=challenge.title,
            description=challenge.description,
            round_id=challenge.round_id,
            is_valid=challenge.is_valid,
            difficulty=challenge.difficulty,
            status=c_status,
        )
        for challenge, c_status in zip(challenges, challenge_status_list)
    ]
    return team_challenges
