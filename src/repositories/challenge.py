from src.repositories.base import Repository
from src.repositories.round import RoundRepository
from src.models.tortoise import Challenge as IChallenge

# 初始化 RoundRepository，並指定模型為 Round
round_repository: RoundRepository = RoundRepository()


class ChallengeRepository(Repository):
    def __init__(self):
        self.model = IChallenge

    async def find_by_id_with_round(self, pk: int):
        # 取得當前 Round
        current_round = await round_repository.get_current_round()
        if not current_round:
            return None
        return await self.model.filter(pk=pk, round=current_round).first()

    async def get_round_by_challenge_id(self, pk: int):
        challenge = await self.model.get(id=pk).prefetch_related("round")
        return challenge.round.id

    def find_all(self):
        return self.model.all()
