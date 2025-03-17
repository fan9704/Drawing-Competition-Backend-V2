from src.dependencies.repositories import get_submission_repository, get_challenge_repository
from src.repositories.challenge import ChallengeRepository
from src.repositories.submission import SubmissionRepository


class SubmissionService:
    def __init__(self, repository: SubmissionRepository= get_submission_repository(), challenge_repository: ChallengeRepository=get_challenge_repository()):
        self.repository = repository
        self.challenge_repository = challenge_repository

    # 建立暫時性的 Submission
    async def create_temperate_submission(self,code: str, team_id: int, challenge_id: int):
        challenge = await self.challenge_repository.get_challenge_by_id_prefetch_round(challenge_id)
        submission = await self.repository.create(
            code=code,
            status="doing",
            team_id=team_id,
            challenge_id=challenge_id,
            round_id=challenge.round.id,
        )
        await submission.save()
        return submission
