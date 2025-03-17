from datetime import datetime, timedelta

import pytest

from src.models.tortoise import Submission, Team, Challenge, Round
from tests.test_fixture import get_testcase_team_one, get_testcase_round_one, get_testcase_challenge_one


class TestSubmissionModel:
    @pytest.mark.asyncio
    async def test_create_submission(self, in_memory_db):
        # 測試創建 Submission 實例
        round_instance: Round = await get_testcase_round_one()
        challenge: Challenge = await get_testcase_challenge_one(round_instance)
        team: Team = await get_testcase_team_one()
        submission: Submission = await Submission.create(
            code="print('Hello World')",
            status="todo",
            score=85,
            fitness=90,
            word_count=20,
            execute_time=timedelta(seconds=120),
            stdout="Success",
            stderr="",
            team=team,
            challenge=challenge,
            round=round_instance,
            draw_image_url="images/submission.png"
        )

        # 查詢並驗證
        result = await Submission.first()
        assert result is not None
        assert result.code == "print('Hello World')"
        assert result.status == "todo"
        assert result.score == 85
        assert result.fitness == 90
        assert result.word_count == 20
        assert result.execute_time == timedelta(seconds=120)
        assert result.stdout == "Success"
        assert result.stderr == ""
        assert result.team == team  # 確認隊伍正確
        assert result.challenge == challenge  # 確認挑戰正確
        assert result.round == round_instance  # 確認回合正確
        assert result.draw_image_url == "images/submission.png"

        await submission.delete()
        await challenge.delete()
        await team.delete()
        await round_instance.delete()

    @pytest.mark.asyncio
    async def test_update_submission(self, in_memory_db):
        # 測試更新 Submission 實例
        round_instance: Round = await get_testcase_round_one()
        challenge: Challenge = await get_testcase_challenge_one(round_instance)
        team: Team = await get_testcase_team_one()
        submission = await Submission.create(
            code="print('Hello World')",
            status="todo",
            score=85,
            fitness=90,
            word_count=20,
            execute_time=timedelta(seconds=120),
            stdout="Success",
            stderr="",
            team=team,
            challenge=challenge,
            round=round_instance,
            draw_image_url="images/submission.png"
        )

        # 更新 submission
        submission.status = "success"
        submission.score = 95
        await submission.save()

        # 查詢並驗證更新
        updated_submission = await Submission.first()
        assert updated_submission.status == "success"
        assert updated_submission.score == 95

        await submission.delete()
        await challenge.delete()
        await round_instance.delete()
        await team.delete()

    @pytest.mark.asyncio
    async def test_delete_submission(self, in_memory_db):
        # 測試刪除 Submission 實例
        round_instance: Round = await get_testcase_round_one()
        challenge: Challenge = await get_testcase_challenge_one(round_instance)
        team: Team = await get_testcase_team_one()
        submission: Submission = await Submission.create(
            code="print('Hello World')",
            status="todo",
            score=85,
            fitness=90,
            word_count=20,
            execute_time=timedelta(seconds=120),
            stdout="Success",
            stderr="",
            team=team,
            challenge=challenge,
            round=round_instance,
            draw_image_url="images/submission.png"
        )

        # 刪除 submission
        await submission.delete()

        # 查詢並驗證
        result = await Submission.first()
        assert result is None  # 確保 Submission 被刪除

        await challenge.delete()
        await round_instance.delete()
        await team.delete()
