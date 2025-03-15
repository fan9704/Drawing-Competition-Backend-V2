import pytest
from tests.conftest import in_memory_db
from src.models.tortoise import Team


class TestTeamModel:
    @pytest.mark.asyncio
    # 測試創建 Team 並檢查資料是否存在
    async def test_create_team(self, in_memory_db):
        team: Team = await Team.create(
            name="第1小隊",
            token="1234"
        )
        await team.save()
        mm = await Team.first()
        assert mm is not None
        assert mm.name == "第1小隊"
        assert mm.token == "1234"

        await team.delete()

    # 測試 Team 的查詢條件
    @pytest.mark.asyncio
    async def test_query_team(self, in_memory_db):
        team1: Team = await Team.create(name="第2小隊", token="5678")
        team2: Team = await Team.create(name="第3小隊", token="abcd")

        team: Team = await Team.get(name="第2小隊")
        assert team is not None
        assert team.name == "第2小隊"
        assert team.token == "5678"

        await team1.delete()
        await team2.delete()

    # 測試更新 Team 資料
    @pytest.mark.asyncio
    async def test_update_team(self, in_memory_db):
        team: Team = await Team.create(name="第4小隊", token="efgh")
        team.name = "第4小隊更新"
        await team.save()

        updated_team: Team = await Team.get(id=team.id)
        assert updated_team.name == "第4小隊更新"

        await team.delete()

    # 測試刪除 Team 資料
    @pytest.mark.asyncio
    async def test_delete_team(self, in_memory_db):
        team: Team = await Team.create(name="第5小隊", token="ijkl")
        await team.delete()

        deleted_team: Team = await Team.filter(id=team.id).first()
        assert deleted_team is None
