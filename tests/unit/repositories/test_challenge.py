import pytest
from unittest.mock import MagicMock, AsyncMock
from src.repositories.round import RoundRepository
from src.repositories.challenge import ChallengeRepository
from src.models.tortoise import Challenge
from src.models.tortoise.round import Round
from tests.test_fixture import get_testcase_round_one, get_testcase_challenge_one


@pytest.mark.asyncio
async def test_find_by_id_with_round(in_memory_db, mocker):
    challenge_repository: ChallengeRepository = ChallengeRepository()
    round_instance: Round = await get_testcase_round_one()
    challenge: Challenge = await get_testcase_challenge_one(round_instance)

    # Mock get_current_round
    mocker.patch.object(RoundRepository, "get_current_round", return_value=round_instance)

    # 執行測試方法
    result = await challenge_repository.find_by_id_with_round(1)

    # 驗證結果
    assert result is not None
    assert result.id == challenge.id
    assert result.round_id == round_instance.id

    await round_instance.delete()
    await challenge.delete()


@pytest.mark.asyncio
async def test_find_by_id_with_round_no_current_round(in_memory_db):
    # 模擬 RoundRepository 的 get_current_round 函數
    round_repository_mock = MagicMock(RoundRepository)
    round_repository_mock.get_current_round = AsyncMock(return_value=None)

    # 初始化 ChallengeRepository
    challenge_repository: ChallengeRepository = ChallengeRepository()
    challenge_repository.model = MagicMock(Challenge)  # 模擬 Challenge 模型

    # 呼叫 find_by_id_with_round 並檢查回傳的結果為 None
    result = await challenge_repository.find_by_id_with_round(1)

    assert result is None


@pytest.mark.asyncio
async def test_get_round_by_challenge_id(in_memory_db, mocker):
    challenge_repository = ChallengeRepository()

    # 創建 Round 物件
    round_obj = await get_testcase_round_one()

    # 創建 Challenge 物件
    challenge_obj = await get_testcase_challenge_one(round_obj)

    # 模擬 Challenge 的 get 方法
    mock_get = mocker.patch.object(Challenge, "get", return_value=challenge_obj)
    mock_get().prefetch_related = mocker.AsyncMock(return_value=challenge_obj)

    # 執行測試方法
    result = await challenge_repository.get_round_by_challenge_id(1)

    # 驗證回傳的 round_id
    assert result == round_obj.id

    await challenge_obj.delete()
    await round_obj.delete()


@pytest.mark.asyncio
async def test_find_all(in_memory_db):
    # 模擬 Challenge 模型的 all 函數
    challenge_mock = MagicMock(Challenge)
    challenge_mock.all = AsyncMock(return_value=[MagicMock(id=1), MagicMock(id=2)])

    # 初始化 ChallengeRepository
    challenge_repository = ChallengeRepository()
    challenge_repository.model = challenge_mock

    # 呼叫 find_all 並檢查結果
    result = await challenge_repository.find_all()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
