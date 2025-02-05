from typing import Optional

from fastapi import APIRouter, Response

from src.models.pydantic import Round, RoundChallengeResponse
from src.models.tortoise import Round as IRound
from src.repositories import RoundRepository

router = APIRouter()
repository: RoundRepository = RoundRepository(IRound)

# RoundListAPIView (列出所有回合)
@router.get("/", response_model=Optional[RoundChallengeResponse])
async def get_all_rounds():
    round_instance = await repository.get_current_round()
    if round_instance:
        # 標註該 Round 已經進行過了
        round_instance.is_valid = True
        await round_instance.save()
        return await RoundChallengeResponse.from_tortoise_orm(round_instance)

    # 檢查是否所有回合結束
    if not await repository.check_valid_round_exists():
        return Response(status_code=204, content="No Content")

    # 檢查是否沒有開放回合
    return Response(status_code=404, content="No round available")

# RoundAPIView (單一回合檢視)
@router.get("/{round_id}", response_model=Round)
async def get_round(round_id: int):
    round_instance = await repository.get_by_id(round_id)
    if round_instance is None:
        return Response(status_code=404, content="Round not found")
    return round_instance