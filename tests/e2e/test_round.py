import pytest

from src.models.tortoise import Round
from tests.test_fixture import get_testcase_round_one, get_testcase_round_two


class TestE2ERound:

    @pytest.mark.asyncio
    async def test_get_all_rounds(self, http_client, in_memory_db):
        round_1: Round = await get_testcase_round_one()
        round_2: Round = await get_testcase_round_two()

        response = await http_client.get("/api/round/")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["is_valid"] == True
        assert response.json()["challenge_list"] == []

        await round_1.delete()
        await round_2.delete()

    @pytest.mark.asyncio
    async def test_get_round(self, http_client, in_memory_db):
        round1: Round = await get_testcase_round_one()

        response = await http_client.get("/api/round/1")

        assert response.status_code == 200
        assert response.json()["is_valid"] == True

        await round1.delete()
