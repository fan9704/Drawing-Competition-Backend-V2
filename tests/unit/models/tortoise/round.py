from datetime import datetime, timedelta

import pytest
from pytz import timezone

from src.models.tortoise import Round  # 根據你的實際導入路徑修改

tz = timezone("Asia/Taipei")

@pytest.mark.asyncio
class TestRoundModel:
    @pytest.mark.asyncio
    async def test_create_round(self, in_memory_db):
        # 測試創建 Round 模型
        start_time = datetime(2025, 3, 3, 9, 0, 0,tzinfo=tz)  # UTC 時間
        end_time = start_time + timedelta(hours=1)

        round = await Round.create(start_time=start_time, end_time=end_time)
        await round.save()

        # 查詢並驗證
        result = await Round.first()
        assert result is not None
        assert result.start_time == start_time
        assert result.end_time == end_time
        assert result.is_valid is True

    @pytest.mark.asyncio
    async def test_get_local_times(self, in_memory_db):
        # 測試時間轉換方法
        start_time = datetime(2025, 3, 3, 9, 0, 0, tzinfo=timezone("UTC"))
        end_time = start_time + timedelta(hours=1)

        round = await Round.create(start_time=start_time, end_time=end_time)

        local_start_time = round.get_local_start_time()
        local_end_time = round.get_local_end_time()

        # 驗證當地時間（台灣時區）是否正確
        assert local_start_time == start_time.astimezone(tz)
        assert local_end_time == end_time.astimezone(tz)

    @pytest.mark.asyncio
    async def test_set_local_times(self, in_memory_db):
        # 測試設置時間轉換
        start_time = datetime(2025, 3, 3, 9, 0, 0, tzinfo=timezone("UTC"))
        end_time = start_time + timedelta(hours=1)

        round = await Round.create(start_time=start_time, end_time=end_time)

        round.set_local_start_time()  # 更新 start_time 為當地時間
        round.set_local_end_time()    # 更新 end_time 為當地時間

        # 查詢並驗證更新
        updated_round = await Round.get(id=round.id)
        assert updated_round.start_time == start_time.astimezone(tz)
        assert updated_round.end_time == end_time.astimezone(tz)