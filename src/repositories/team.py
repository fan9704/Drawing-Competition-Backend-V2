from src.repositories.base import Repository

class TeamRepository(Repository):
    async def get_team_by_token(self, token: str):
        return await self.model.filter(token=token).first()