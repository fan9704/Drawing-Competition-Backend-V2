import pytest

from src.models.tortoise import Team
from tests.test_fixture import get_testcase_team_one, get_testcase_team_two


class TestE2ETeam:

    @pytest.mark.asyncio
    async def test_list(self, http_client, in_memory_db):
        team1: Team = await get_testcase_team_one()
        team2: Team = await get_testcase_team_two()

        response = await http_client.get("/api/team/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        await team1.delete()
        await team2.delete()

    @pytest.mark.asyncio
    async def test_get_team_by_token(self, http_client, in_memory_db):
        team1: Team = await get_testcase_team_one()
        token: str = "ABCD"
        response = await http_client.get(f"/api/team/{token}/")
        assert response.status_code == 200
        assert response.json()["name"] == "第1小隊"
        await team1.delete()

    @pytest.mark.asyncio
    async def test_auth_team(self, http_client, in_memory_db):
        team1: Team = await get_testcase_team_one()
        body = {
            "token": "ABCD"
        }

        response = await http_client.post(
            url="/api/team/auth/token/",
            json=body
        )

        assert response.status_code == 200
        assert response.json()["status"] == True
        assert response.json()["team"]["id"] == 1
        assert response.json()["team"]["name"] == "第1小隊"
        assert response.json()["access_token"] is not None

        await team1.delete()
