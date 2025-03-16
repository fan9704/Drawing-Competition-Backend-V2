import pytest

from src.models.tortoise import Challenge, Round,Team, Submission
from tests.test_fixture import get_testcase_challenge_one, get_testcase_challenge_two, get_testcase_round_one,get_testcase_team_one,get_testcase_submission_one,get_testcase_submission_two


class TestE2EChallenge:
    # @classmethod
    # async def setup_class(cls):
    #     # Class 啟動前執行
    #     round1: Round = await get_testcase_round_one()
    #     challenge1: Challenge = await get_testcase_challenge_one(round1)
    #
    # @classmethod
    # async def teardown_class(cls):
    #     await Challenge.delete()
    #     await Round.delete()
    @pytest.mark.asyncio
    async def test_get_all_challenge(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        challenge2: Challenge = await get_testcase_challenge_two(round1)

        response = await http_client.get("/api/challenge/")

        assert response.status_code == 200
        assert len(response.json()) == 2

        await challenge1.delete()
        await challenge2.delete()
        await round1.delete()

    @pytest.mark.asyncio
    async def test_get_challenge_by_id(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)

        response = await http_client.get("/api/challenge/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["title"] == "題目一 苦力怕"
        assert response.json()["description"] == "嘶嘶苦力怕"
        assert response.json()["difficulty"] == "easy"
        assert response.json()["is_valid"] == True
        assert response.json()["image_url"] == "images/default.png"
        assert response.json()["round_id"] == 1

        await challenge1.delete()
        await round1.delete()

    @pytest.mark.asyncio
    async def test_list_challenges_by_team(self,http_client,in_memory_db):
        team1: Team = await get_testcase_team_one()
        round1: Round = await get_testcase_round_one()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        challenge2: Challenge = await get_testcase_challenge_two(round1)
        submission1: Submission = await get_testcase_submission_one(round1,team1,challenge1)
        submission2: Submission = await get_testcase_submission_two(round1,team1,challenge2)

        response = await http_client.get("/api/challenge/team/1")

        assert response.status_code == 200
        assert len(response.json()) == 2

        await submission1.delete()
        await submission2.delete()
        await challenge1.delete()
        await challenge2.delete()
        await team1.delete()
        await round1.delete()