from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.models.pydantic import ChallengeWithOutRelationPydantic
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
    response_model=List[ChallengeWithOutRelationPydantic]
)
async def get_all_challenges(repository: ChallengeRepository = Depends(get_challenge_repository)):
    return await ChallengeWithOutRelationPydantic.from_queryset(repository.find_all())

# 取得單一挑戰 (根據 ID)
@router.get("/{pk}", response_model=Challenge)
async def get_challenge_by_id(
    pk: int,
    repository: ChallengeRepository = Depends(get_challenge_repository)
) -> Challenge:
    challenge = await repository.find_by_id_with_round(pk=pk)
    if challenge:
        return challenge
    raise HTTPException(status_code=400, detail="Challenge is not valid")

# 根據 team_id 列出挑戰
# TODO: Change Frontend Route
@router.get("/team/{team_id}", response_model=List[ChallengeTeamSubmissionResponse])
async def list_challenges_by_team(
    team_id: int = None,
    repository: ChallengeRepository = Depends(get_challenge_repository),
    submission_repository: SubmissionRepository = Depends(get_submission_repository),
) -> List[ChallengeTeamSubmissionResponse]:
    if team_id is None:
        raise HTTPException(status_code=400, detail="team_id is required")

    challenges = await repository.filter()
    challenge_status_list = []
    for challenge in challenges:
        challenge_status =  await submission_repository.filter_submission_by_challenge(team_id, challenge)
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