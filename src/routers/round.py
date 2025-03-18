from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.dependencies import get_round_service
from src.models.pydantic import Round, RoundChallengeResponse
from src.services import RoundService

router = APIRouter()


# RoundListAPIView (列出所有回合)
@router.get("/",
            summary="取得當前回合",
            description="Get Current Round Challenge",
            response_model=Optional[RoundChallengeResponse],
            response_description="Current Round Challenge"
            )
@cache(expire=10)
async def get_all_rounds(service: RoundService = Depends(get_round_service)) -> (
        Optional)[RoundChallengeResponse]:
    return await service.get_all_rounds()


# RoundAPIView (單一回合檢視)
@router.get("/{round_id}",
            summary="取得該回合資訊",
            description="Get Round Information",
            response_model=Round,
            response_description="Round Information"
            )
@cache(expire=10)
async def get_round(round_id: int, service: RoundService = Depends(get_round_service)) -> Optional[Round]:
    return await service.get_round(round_id)
