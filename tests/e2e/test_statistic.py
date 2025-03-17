import pytest

from src.models.tortoise import Challenge, Round, Team, Submission
from tests.test_fixture import get_testcase_challenge_one, get_testcase_challenge_two, get_testcase_round_one, \
    get_testcase_team_one, get_testcase_submission_one, get_testcase_submission_two, get_testcase_team_two


class TestE2EStatistic(object):
    @classmethod
    async def setup_class(cls):
        # Class 啟動前執行
        round1: Round = await get_testcase_round_one()
        team1: Team = await get_testcase_team_one()
        team2: Team = await get_testcase_team_two()
        challenge1: Challenge = await get_testcase_challenge_one(round1)
        submission1: Submission = await get_testcase_submission_one(round1, team1, challenge1)
        submission2: Submission = await get_testcase_submission_two(round1, team2, challenge1)
        submission3: Submission = await get_testcase_submission_one(round1, team1, challenge1)

    @classmethod
    async def teardown_class(cls):
        # Class 執行完成後執行
        await Submission.delete()
        await Challenge.delete()
        await Round.delete()
        await Team.delete()

    async def setup_method(self, method):
        # 每個 method 執行前執行
        pass

    async def teardown_method(self, method):
        # 每個 method 執行結束後執行
        pass

    @pytest.mark.asyncio
    async def test_get_team_challenge_highest_score(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/team/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_team_challenge_submission_count(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/count/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_team_round_total_score(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/round/1/team/?team_id=1"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_team_round_all_teams(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/round/allTeam/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_all_team_single_round_total_score(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/round/1/allTeam/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_top3_team_challenge_score(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/challenge/1/top3Team/"
        )
        logger.info(f"Response: {response.text}")

        # assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_all_success_submission_by_challenge_id_and_team_id(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/challenge/1/team/1/success/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_all_team_success_submission_challenge_id(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/challenge/1/allTeam/success/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_all_challenge_featured_submission(self, http_client, in_memory_db, logger):
        response = await http_client.get(
            url="/api/statistic/challenge/all/featured/allTeam/success/"
        )
        logger.info(f"Response: {response.text}")

        assert response.status_code == 200
