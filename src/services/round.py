from typing import Optional

from fastapi import HTTPException

from src.models.tortoise import Round
from src.utils.i18n import _
from src.dependencies import get_round_repository
from src.models.pydantic import ChallengePydantic, RoundChallengeResponse
from src.repositories import RoundRepository


class RoundService:
    def __init__(self, repository: RoundRepository = get_round_repository()):
        self.repository = repository

    # 取得當前 round
    async def get_all_rounds(self) -> Optional[RoundChallengeResponse]:
        round_instance = await self.repository.get_current_round()
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
        elif not await self.repository.check_valid_round_exists():
            # 檢查是否所有回合結束
            raise HTTPException(status_code=204, detail=_("No Content"))
        else:
            # 檢查是否沒有開放回合
            raise HTTPException(status_code=404, detail=_("No round available"))

    # 取得 Round By round_id
    async def get_round(self, round_id: int) -> Optional[Round]:
        return await self.repository.get_by_id(round_id)