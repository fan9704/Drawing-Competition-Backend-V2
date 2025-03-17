import pytest

from src.models.tortoise import Challenge, Round, Team, Submission
from tests.test_fixture import get_testcase_challenge_one, get_testcase_challenge_two, get_testcase_round_one, \
    get_testcase_team_one, get_testcase_submission_one, get_testcase_submission_two


class TestE2ESubmission:
    @pytest.mark.asyncio
    async def test_store_submission(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        submission1: Submission = await  get_testcase_submission_one(round1, team1, challenge1)

        body = {
            "score": 90,
            "fitness": 90,
            "word_count": 200,
            "execute_time": 0,
            "stdout": "",
            "stderr": "",
            "status": "success"
        }

        response = await http_client.post(
            url="/api/submission/store/1/",
            json=body
        )

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["team_id"] == 1
        assert response.json()["score"] == 90
        assert response.json()["fitness"] == 90
        assert response.json()["word_count"] == 200
        assert response.json()["stdout"] == ""
        assert response.json()["stderr"] == ""
        assert response.json()["status"] == "success"
        assert response.json()["draw_image_url"] == "/media/result/1/team_1/1.png"
        assert response.json()["challenge_id"] == 1
        assert response.json()["round_id"] == 1

        await submission1.delete()
        await challenge1.delete()
        await round1.delete()
        await team1.delete()

    @pytest.mark.asyncio
    async def test_submit_code(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)

        data = {
            "code": "import turtle",
            "team": 1,
            "challenge": 1
        }
        response = await http_client.post(
            url="/api/submission/",
            json=data
        )

        assert response.status_code == 200
        assert response.json()["team"] == 1
        assert response.json()["round"] == 1
        assert response.json()["challenge"] == 1
        assert response.json()["status"] == "success"

        await challenge1.delete()
        await round1.delete()
        await team1.delete()

    @pytest.mark.asyncio
    async def test_get_submissions_by_team_and_challenge(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        submission1: Submission = await get_testcase_submission_one(round1, team1, challenge1)
        submission2: Submission = await get_testcase_submission_two(round1, team1, challenge1)

        response = await http_client.get(
            url="/api/submission/all/1/1/"
        )

        assert response.status_code == 200
        assert len(response.json()) == 2

        await submission1.delete()
        await submission2.delete()
        await challenge1.delete()
        await round1.delete()
        await team1.delete()

    @pytest.mark.asyncio
    async def test_get_highest_score_submission(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        submission1: Submission = await get_testcase_submission_one(round1, team1, challenge1)
        submission2: Submission = await get_testcase_submission_two(round1, team1, challenge1)

        response = await http_client.get(
            url="/api/submission/max/1/1/"
        )

        assert response.status_code == 200
        assert response.json()["score"] == 82
        assert response.json()["fitness"] == 82
        assert response.json()["status"] == "success"
        assert response.json()["word_count"] == 76
        assert response.json()["stdout"] == ""
        assert response.json()["stderr"] == ""

        await submission1.delete()
        await submission2.delete()
        await challenge1.delete()
        await round1.delete()
        await team1.delete()

    @pytest.mark.asyncio
    async def test_get_all_submissions_by_team(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        submission1: Submission = await  get_testcase_submission_one(round1, team1, challenge1)
        submission2: Submission = await  get_testcase_submission_two(round1, team1, challenge1)

        response = await http_client.get(
            url="/api/submission/team/1/"
        )

        assert response.status_code == 200
        assert len(response.json()) == 2

        await submission1.delete()
        await submission2.delete()
        await challenge1.delete()
        await round1.delete()
        await team1.delete()
