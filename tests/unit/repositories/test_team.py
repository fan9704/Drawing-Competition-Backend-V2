import pytest
from src.repositories.team import TeamRepository
from src.models.tortoise.team import Team
from tests.test_fixture import get_testcase_team_one, get_testcase_team_two


@pytest.mark.asyncio
async def test_get_team_by_token(in_memory_db):
    team_repository: TeamRepository = TeamRepository()
    team: Team = await get_testcase_team_one()

    # 執行測試方法
    result = await team_repository.get_team_by_token("ABCD")

    # 驗證結果
    assert result is not None
    assert result.id == team.id
    assert result.name == "第1小隊"
    assert result.token == "ABCD"

    await team.delete()


@pytest.mark.asyncio
async def test_get_team_by_token_not_found(in_memory_db):
    team_repository: TeamRepository = TeamRepository()
    team: Team = await get_testcase_team_two()
    result = await team_repository.get_team_by_token("KJLN")

    # 驗證應該回傳 None
    assert result is None

    await team.delete()
