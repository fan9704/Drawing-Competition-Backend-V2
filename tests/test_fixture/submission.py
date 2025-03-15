from src.models.tortoise import Submission, Round, Team, Challenge
from src.models.enums import StatusEnum
from datetime import timedelta


async def get_testcase_submission_one(round_instance: Round, team: Team, challenge: Challenge):
    return await Submission.create(
        id=1,
        code="import turtle",
        status=StatusEnum.success,
        score=82.0,
        fitness=82.0,
        word_count=76,
        execute_time=timedelta(seconds=3600),
        team=team,
        challenge=challenge,
        round=round_instance,
    )


async def get_testcase_submission_two(round_instance: Round, team: Team, challenge: Challenge):
    return await Submission.create(
        id=2,
        code="import turtle as t",
        status=StatusEnum.success,
        score=18.0,
        fitness=18.0,
        word_count=53,
        execute_time=timedelta(seconds=3600),
        team=team,
        challenge=challenge,
        round=round_instance,
    )
