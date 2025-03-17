from datetime import datetime

import pytest

from src.models.tortoise import Challenge, Round


class TestChallengeModel:
    @pytest.mark.asyncio
    async def test_create_challenge(self, in_memory_db):
        # 測試創建 Challenge 實例
        round_instance: Round = await Round.create(
            start_time=datetime(2025, 3, 3, 9, 0),
            end_time=datetime(2025, 3, 3, 10, 0)
        )

        challenge: Challenge = await Challenge.create(
            title="Test Challenge",
            description="This is a test challenge.",
            image_url="images/test.png",
            difficulty="medium",
            round=round_instance,
        )

        # 查詢並驗證
        result: Challenge = await Challenge.first()
        assert result is not None
        assert result.title == "Test Challenge"
        assert result.description == "This is a test challenge."
        assert result.difficulty == "medium"
        assert result.image_url == "images/test.png"
        #TODO Check Round Instance
        await challenge.delete()
        await round_instance.delete()

    @pytest.mark.asyncio
    async def test_update_challenge(self, in_memory_db):
        # 測試更新 Challenge 實例
        round_instance: Round = await Round.create(
            start_time=datetime(2025, 3, 3, 9, 0),
            end_time=datetime(2025, 3, 3, 10, 0)
        )

        challenge: Challenge = await Challenge.create(
            title="Test Challenge",
            description="This is a test challenge.",
            image_url="images/test.png",
            difficulty="easy",
            round=round_instance,
        )

        # 更新 challenge
        challenge.title = "Updated Challenge"
        challenge.description = "This is an updated test challenge."
        await challenge.save()

        # 查詢並驗證更新
        updated_challenge = await Challenge.first()
        assert updated_challenge.title == "Updated Challenge"
        assert updated_challenge.description == "This is an updated test challenge."

        await challenge.delete()
        await round_instance.delete()
    @pytest.mark.asyncio
    async def test_delete_challenge(self, in_memory_db):
        # 測試刪除 Challenge 實例
        round_instance: Round = await Round.create(
            start_time=datetime(2025, 3, 3, 9, 0),
            end_time=datetime(2025, 3, 3, 10, 0)
        )

        challenge: Challenge = await Challenge.create(
            title="Test Challenge",
            description="This is a test challenge.",
            image_url="images/test.png",
            difficulty="easy",
            round=round_instance,
        )

        # 刪除 challenge
        await challenge.delete()

        # 查詢並驗證
        result: Challenge = await Challenge.first()
        assert result is None  # 確保 Challenge 被刪除

        await round_instance.delete()