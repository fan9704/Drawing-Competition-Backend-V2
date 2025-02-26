from typing import Optional

from fastapi import APIRouter, Response, HTTPException

from src.models.pydantic import Round, RoundChallengeResponse, ChallengePydantic
from src.repositories import RoundRepository

router = APIRouter()
repository: RoundRepository = RoundRepository()

# RoundListAPIView (列出所有回合)
@router.get("/",
            summary="取得當前回合",
            description="Get Current Round Challenge",
            response_model=Optional[RoundChallengeResponse],
            response_description="Current Round Challenge"
)
async def get_all_rounds() -> Optional[RoundChallengeResponse]:
    round_instance = await repository.get_current_round()
    if round_instance:
        # 標註該 Round 已經進行過了
        round_instance.is_valid = True
        await round_instance.save()
        challenges = await ChallengePydantic.from_queryset(round_instance.challenge_list.all())
        return RoundChallengeResponse(
            id=round_instance.id,
            start_time=round_instance.start_time,
            end_time=round_instance.end_time,
            is_valid=round_instance.is_valid,
            challenge_list=challenges
        )
    elif not await repository.check_valid_round_exists():
        # 檢查是否所有回合結束
        raise HTTPException(status_code=204, detail="No Content")
    else:
        # 檢查是否沒有開放回合
        raise HTTPException(status_code=404, detail="No round available")

# RoundAPIView (單一回合檢視)
@router.get("/{round_id}",
            summary="取得該回合資訊",
            description="Get Round Information",
            response_model=Round,
            response_description="Round Information"
)
async def get_round(round_id: int) -> Optional[Round]:
    round_instance = await repository.get_by_id(round_id)
    if round_instance is None:
        raise HTTPException(status_code=404, detail="Round not found")
    return round_instance