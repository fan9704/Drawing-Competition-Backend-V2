from src.repositories.base import Repository
from src.models.tortoise.team import Team as ITeam


class TeamRepository(Repository):
    def __init__(self):
        self.model = ITeam

    async def get_team_by_token(self, token: str):
        return await self.model.filter(token=token).first()
