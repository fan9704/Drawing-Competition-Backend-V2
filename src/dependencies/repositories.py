from src.repositories import RoundRepository, ChallengeRepository, SubmissionRepository, TeamRepository


def get_round_repository() -> RoundRepository:
    return RoundRepository()


def get_challenge_repository() -> ChallengeRepository:
    return ChallengeRepository()


def get_submission_repository() -> SubmissionRepository:
    return SubmissionRepository()


def get_team_repository() -> TeamRepository:
    return TeamRepository()
