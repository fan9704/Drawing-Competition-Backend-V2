from src.repositories.base import Repository
from src.repositories.round import RoundRepository
from src.models.tortoise import Round

# 初始化 RoundRepository，並指定模型為 Round
round_repository: RoundRepository = RoundRepository(Round)

class ChallengeRepository(Repository):
    async def find_by_id_with_round(self, pk: int):
        # 取得當前 Round
        current_round = await round_repository.get_current_round()
        if not current_round:
            return None
        # 假設 Challenge 模型的外鍵欄位名稱為 round，
        # 可依需求改成 filter(round_id=current_round.id)
        return await self.model.filter(pk=pk, round=current_round).first()

    async def get_round_by_challenge_id(self, pk: int):
        challenge = await self.model.get(id=pk).prefetch_related("round")
        return challenge.round.id