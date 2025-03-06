import pytest
import datetime
from pydantic import ValidationError
from src.models.pydantic.round import Round, RoundChallengeResponse
from src.models.pydantic.challenge import ChallengePydantic
from src.models.enums import DifficultyEnum


# ✅ 測試 Round Model 正常建立
def test_create_round():
    start_time = datetime.datetime(2025, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime(2025, 3, 3, 10, 0, tzinfo=datetime.timezone.utc)

    round_instance = Round(
        start_time=start_time,
        end_time=end_time,
        is_valid=True
    )

    assert round_instance.start_time == start_time
    assert round_instance.end_time == end_time
    assert round_instance.is_valid is True


# ✅ 測試 Round Model 預設值
def test_round_default_values():
    start_time = datetime.datetime(2025, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime(2025, 3, 3, 10, 0, tzinfo=datetime.timezone.utc)

    round_instance = Round(
        start_time=start_time,
        end_time=end_time
    )

    assert round_instance.is_valid is True  # 預設值應該是 True


# ❌ 測試 Round Model 驗證錯誤（start_time 應該是 datetime）
def test_round_validation_error():
    with pytest.raises(ValidationError):
        Round(
            start_time="not_a_datetime",  # 錯誤類型
            end_time="2025-03-03T10:00:00Z",
            is_valid=True
        )


# ✅ 測試 RoundChallengeResponse Model 正常建立
def test_create_round_challenge_response():
    start_time = datetime.datetime(2025, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime(2025, 3, 3, 10, 0, tzinfo=datetime.timezone.utc)

    challenge = ChallengePydantic(
        id=1,
        title="測試題目",
        description="這是一個測試題目",
        image_url="/images/test.png",
        difficulty=DifficultyEnum.easy,
        is_valid=True
    )

    round_response = RoundChallengeResponse(
        id=100,
        start_time=start_time,
        end_time=end_time,
        is_valid=False,
        challenge_list=[challenge]
    )

    assert round_response.id == 100
    assert round_response.start_time == start_time
    assert round_response.end_time == end_time
    assert round_response.is_valid is False
    assert len(round_response.challenge_list) == 1
    assert round_response.challenge_list[0].title == "測試題目"


# ✅ 測試 RoundChallengeResponse 預設值
def test_round_challenge_response_default_values():
    start_time = datetime.datetime(2025, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime(2025, 3, 3, 10, 0, tzinfo=datetime.timezone.utc)

    round_response = RoundChallengeResponse(
        id=101,
        start_time=start_time,
        end_time=end_time,
        challenge_list=[]
    )

    assert round_response.is_valid is True  # 預設應該是 True
    assert len(round_response.challenge_list) == 0  # 預設空列表


# ❌ 測試 RoundChallengeResponse 驗證錯誤（challenge_list 應該是 List）
def test_round_challenge_response_validation_error():
    start_time = datetime.datetime(2025, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime(2025, 3, 3, 10, 0, tzinfo=datetime.timezone.utc)

    with pytest.raises(ValidationError):
        RoundChallengeResponse(
            id=102,
            start_time=start_time,
            end_time=end_time,
            is_valid=True,
            challenge_list="not_a_list"  # 錯誤類型
        )
