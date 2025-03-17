from src.dependencies import get_challenge_repository
from src.repositories import ChallengeRepository


class ChallengeService:
    def __init__(self,repository:ChallengeRepository=get_challenge_repository()):
        self.repository = repository