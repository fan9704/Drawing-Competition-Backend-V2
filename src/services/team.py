from src.dependencies import get_team_repository
from src.repositories import TeamRepository


class TeamService:
    def __init__(self,repository:TeamRepository=get_team_repository()):
        self.repository = repository