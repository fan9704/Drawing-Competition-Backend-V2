from datetime import datetime, timedelta

import pytest

from src.models.tortoise import Round
from src.repositories.round import RoundRepository
from tests.test_fixture import get_testcase_round_one, get_testcase_round_two


@pytest.mark.asyncio
async def test_get_current_round(in_memory_db):
    round_repository: RoundRepository = RoundRepository()
    round_instance: Round = await get_testcase_round_one()

    result = await round_repository.get_current_round()

    assert result is not None
    assert result.id == round_instance.id

    await round_instance.delete()


@pytest.mark.asyncio
async def test_check_valid_round_exists(in_memory_db):
    round_repository: RoundRepository = RoundRepository()

    # 創建測試用的 Round 物件
    round_instance: Round = await get_testcase_round_two()

    result = await round_repository.check_valid_round_exists()

    assert result is True
    await round_instance.delete()


@pytest.mark.asyncio
async def test_find_all_valid_round(in_memory_db):
    round_repository = RoundRepository()

    # 創建測試用的 Round 物件
    valid_round: Round = await Round.create(start_time=datetime(2025, 3, 3, 9, 0, 0),
                                            end_time=datetime(2025, 3, 3, 12, 0, 0),
                                            is_valid=True)
    invalid_round: Round = await Round.create(start_time=datetime(2025, 3, 3, 13, 0, 0),
                                              end_time=datetime(2025, 3, 3, 16, 0, 0),
                                              is_valid=False)

    result = await round_repository.find_all_valid_round()

    assert len(result) == 1
    assert result[0].id == valid_round.id

    await valid_round.delete()
    await invalid_round.delete()
