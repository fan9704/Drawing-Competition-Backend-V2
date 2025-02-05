from src.repositories.base import Repository


from datetime import datetime
class RoundRepository(Repository):
    # 取得當前 Round
    async def get_current_round(self):
        return await self.model.filter(
            start_time__lte=datetime.now(),
            end_time__gte=datetime.now()
        ).prefetch_related("challenge_list").first()
    # 檢查當前是否有有效 Round
    async def check_valid_round_exists(self):
            exists = await self.model.filter(is_valid=False).exists()
            print(">>>", exists)
            return exists
    # 取得所有有效 Round
    async def find_all_valid_round(self):
            return await self.model.filter(is_valid=True)