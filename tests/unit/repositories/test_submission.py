import pytest

from src.models.tortoise import Submission, Team, Round, Challenge
from src.repositories import SubmissionRepository
from tests.test_fixture import get_testcase_team_one, get_testcase_round_one, get_testcase_challenge_one, \
    get_testcase_submission_one


@pytest.mark.asyncio
async def test_get_last_submission(in_memory_db):
    team: Team = await get_testcase_team_one()
    round_instance: Round = await get_testcase_round_one()
    challenge: Challenge = await get_testcase_challenge_one(round_instance=round_instance)
    submission: Submission = await get_testcase_submission_one(
        round_instance=round_instance,
        challenge=challenge,
        team=team
    )

    submission_repository: SubmissionRepository = SubmissionRepository()
    result = await submission_repository.get_last_submission()

    assert result == submission

    await team.delete()
    await round_instance.delete()
    await challenge.delete()
    await submission.delete()


@pytest.mark.asyncio
async def test_find_newest_submission_by_team_id(in_memory_db):
    team: Team = await get_testcase_team_one()
    round_instance: Round = await get_testcase_round_one()
    challenge: Challenge = await get_testcase_challenge_one(round_instance=round_instance)
    submission: Submission = await get_testcase_submission_one(
        round_instance=round_instance,
        challenge=challenge,
        team=team
    )
    submission_repository: SubmissionRepository = SubmissionRepository()
    result = await submission_repository.find_newest_submission_by_team_id(1)

    assert result == submission

    await team.delete()
    await round_instance.delete()
    await challenge.delete()
    await submission.delete()


@pytest.mark.asyncio
async def test_find_all_submission_by_challenge_id_and_team_id(in_memory_db):
    team: Team = await get_testcase_team_one()
    round_instance: Round = await get_testcase_round_one()
    challenge: Challenge = await get_testcase_challenge_one(round_instance=round_instance)
    submission: Submission = await get_testcase_submission_one(
        round_instance=round_instance,
        challenge=challenge,
        team=team
    )
    submission_repository: SubmissionRepository = SubmissionRepository()
    result = await submission_repository.find_all_submission_by_challenge_id_and_team_id(1, 1)

    assert result == [submission]

    await team.delete()
    await round_instance.delete()
    await challenge.delete()
    await submission.delete()


@pytest.mark.asyncio
async def test_find_max_score_submission_by_challenge_id_and_team_id(in_memory_db):
    team: Team = await get_testcase_team_one()
    round_instance: Round = await get_testcase_round_one()
    challenge: Challenge = await get_testcase_challenge_one(round_instance=round_instance)
    submission: Submission = await get_testcase_submission_one(
        round_instance=round_instance,
        challenge=challenge,
        team=team
    )
    submission_repository: SubmissionRepository = SubmissionRepository()
    result = await submission_repository.find_max_score_submission_by_challenge_id_and_team_id(1, 1)

    assert result == submission

    await team.delete()
    await round_instance.delete()
    await challenge.delete()
    await submission.delete()
