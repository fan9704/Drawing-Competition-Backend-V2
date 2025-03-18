from src.services.round import RoundService
from src.services.challenge import ChallengeService
from src.services.team import TeamService
from src.services.statistic import StatisticService
from src.services.submission import SubmissionService


def get_submission_service() -> SubmissionService:
    return SubmissionService()


def get_statistic_service() -> StatisticService:
    return StatisticService()


def get_team_service() -> TeamService:
    return TeamService()


def get_challenge_service() -> ChallengeService:
    return ChallengeService()


def get_round_service() -> RoundService:
    return RoundService
