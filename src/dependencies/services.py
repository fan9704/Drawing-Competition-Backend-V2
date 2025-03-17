from src.services import SubmissionService,StatisticService,ChallengeService,TeamService


def get_submission_service() -> SubmissionService:
    return SubmissionService()

def get_statistic_service() -> StatisticService:
    return StatisticService()

def get_team_service() -> TeamService:
    return TeamService()

def get_challenge_service() -> ChallengeService:
    return ChallengeService()