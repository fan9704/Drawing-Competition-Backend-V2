from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from src.models.enums import StatusEnum
from src.models.pydantic.challenge import Challenge
from src.models.pydantic.statistic import (
    StatisticTeamChallengeScoreResponseDTO,
    StatisticTeamChallengeSubmissionCountResponseDTO,
    StatisticTeamRoundTotalScoreResponseDTO,
    StatisticAllTeamSingleRoundTotalScoreResponseDTO,
    StatisticAllTeamRoundTotalScoreResponseDTO,
    StatisticTop3TeamChallengeScoreResponseDTO,
    StatisticOneLayerSubmissionResponseDTO,
    StatisticFeaturedSubmissionResponseDTO,
)


# ✅ 測試 StatisticTeamChallengeScoreResponseDTO 正常建立
def test_create_statistic_team_challenge_score():
    response = StatisticTeamChallengeScoreResponseDTO(
        challenge=1,
        team_id=2,
        max_score=95,
        submission=None
    )

    assert response.challenge == 1
    assert response.team_id == 2
    assert response.max_score == 95


# ❌ 測試 max_score 小於 0 時拋出錯誤
def test_statistic_team_challenge_score_invalid_max_score():
    with pytest.raises(ValidationError):
        StatisticTeamChallengeScoreResponseDTO(
            challenge=1,
            team_id=2,
            max_score=-10,
            submission=None
        )


# ✅ 測試 StatisticTeamChallengeSubmissionCountResponseDTO 正常建立
def test_create_statistic_team_challenge_submission_count():
    response = StatisticTeamChallengeSubmissionCountResponseDTO(
        challenge=1,
        submission_count=3
    )

    assert response.challenge == 1
    assert response.submission_count == 3


# ❌ 測試 submission_count 小於 0 時拋出錯誤
def test_statistic_team_challenge_submission_count_invalid():
    with pytest.raises(ValidationError):
        StatisticTeamChallengeSubmissionCountResponseDTO(
            challenge=1,
            submission_count=-1
        )


# ✅ 測試 StatisticTeamRoundTotalScoreResponseDTO 正常建立
def test_create_statistic_team_round_total_score():
    response = StatisticTeamRoundTotalScoreResponseDTO(
        round_id=1,
        team_id=2,
        total_score=150
    )

    assert response.round_id == 1
    assert response.team_id == 2
    assert response.total_score == 150


# ✅ 測試 StatisticAllTeamSingleRoundTotalScoreResponseDTO 正常建立
def test_create_statistic_all_team_single_round_total_score():
    response = StatisticAllTeamSingleRoundTotalScoreResponseDTO(
        team_id=3,
        team_name="第1小隊",
        total_score=200,
        score_list=[100, 50, 50]
    )

    assert response.team_id == 3
    assert response.team_name == "第1小隊"
    assert response.total_score == 200
    assert response.score_list == [100, 50, 50]


# ✅ 測試 StatisticAllTeamRoundTotalScoreResponseDTO 正常建立
def test_create_statistic_all_team_round_total_score():
    response = StatisticAllTeamRoundTotalScoreResponseDTO(
        team_id=4,
        team_name="第2小隊",
        round_id_list=[1, 2, 3],
        total_score_list=[90, 85, 95]
    )

    assert response.team_id == 4
    assert response.team_name == "第2小隊"
    assert response.round_id_list == [1, 2, 3]
    assert response.total_score_list == [90, 85, 95]


# ✅ 測試 StatisticTop3TeamChallengeScoreResponseDTO 正常建立
def test_create_statistic_top3_team_challenge_score():
    response = StatisticTop3TeamChallengeScoreResponseDTO(
        team=5,
        team_name="冠軍隊伍",
        max_score=100,
        fitness=98.5,
        execute_time=timedelta(seconds=3),
        word_count=500
    )

    assert response.team == 5
    assert response.team_name == "冠軍隊伍"
    assert response.max_score == 100
    assert response.fitness == 98.5
    assert response.execute_time == timedelta(seconds=3)
    assert response.word_count == 500


# ❌ 測試 fitness 超過範圍 (應在 0.0 - 100.0 之間)
def test_statistic_top3_team_challenge_score_invalid_fitness():
    with pytest.raises(ValidationError):
        StatisticTop3TeamChallengeScoreResponseDTO(
            team=5,
            team_name="冠軍隊伍",
            max_score=100,
            fitness=111.5,  # 錯誤範圍
            execute_time=timedelta(seconds=3),
            word_count=500
        )


# ✅ 測試 StatisticOneLayerSubmissionResponseDTO 正常建立
def test_create_statistic_one_layer_submission():
    response = StatisticOneLayerSubmissionResponseDTO(
        id=10,
        team_id=2,
        score=85,
        code="print('Hello, World!')",
        fitness=90,
        word_count=120,
        execution_time=2,
        stdout="Hello, World!",
        stderr="",
        status=StatusEnum.success,
        draw_image_url="images/result.png",
        time=datetime.now(),
        challenge_id=1,
        round_id=1
    )

    assert response.id == 10
    assert response.score == 85
    assert response.stdout == "Hello, World!"


# ✅ 測試 StatisticFeaturedSubmissionResponseDTO 正常建立
def test_create_statistic_featured_submission():
    challenge_instance = Challenge(
        id=1,
        title="測試題目",
        description="這是一個測試用的題目",
        round_id=1,
        is_valid=True
    )

    submission_instance = StatisticOneLayerSubmissionResponseDTO(
        id=20,
        team_id=5,
        score=95,
        code="print('Python!')",
        fitness=99,
        word_count=250,
        execution_time=1,
        stdout="Python!",
        stderr="",
        status=StatusEnum.success,
        draw_image_url="images/output.png",
        time=datetime.now(),
        challenge_id=1,
        round_id=2
    )

    response = StatisticFeaturedSubmissionResponseDTO(
        challenge=challenge_instance,
        submissions=[submission_instance]
    )

    assert response.challenge.id == 1
    assert response.challenge.title == "測試題目"
    assert len(response.submissions) == 1
    assert response.submissions[0].score == 95
