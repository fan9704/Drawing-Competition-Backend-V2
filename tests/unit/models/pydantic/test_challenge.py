import pytest
from pydantic import ValidationError
from src.models.pydantic import Challenge, ChallengeTeamSubmissionResponse
from src.models.enums import DifficultyEnum, StatusEnum


def test_create_challenge():
    challenge = Challenge(
        id=1,
        title="題目名稱",
        description="這是一個測試題目",
        image_url="/images/test.png",
        difficulty=DifficultyEnum.hard,
        round_id=10,
        is_valid=True
    )

    assert challenge.id == 1
    assert challenge.title == "題目名稱"
    assert challenge.description == "這是一個測試題目"
    assert challenge.image_url == "/images/test.png"
    assert challenge.difficulty == DifficultyEnum.hard
    assert challenge.round_id == 10
    assert challenge.is_valid is True


def test_challenge_default_values():
    challenge = Challenge(
        id=2,
        title="預設測試",
        description="預設值測試",
        round_id=5,
        is_valid=False
    )

    assert challenge.image_url == "/images/default.png"
    assert challenge.difficulty == DifficultyEnum.easy  # 預設為 easy


def test_challenge_validation_error():
    with pytest.raises(ValidationError):
        Challenge(
            id="wrong_type",  # id 應該是 int
            title="測試錯誤",
            description="這應該失敗",
            round_id=1,
            is_valid=True
        )


def test_create_challenge_submission_response():
    submission = ChallengeTeamSubmissionResponse(
        id=3,
        title="提交測試",
        description="這是一個提交測試",
        round_id=7,
        is_valid=True,
        difficulty=DifficultyEnum.medium,
        status=StatusEnum.success
    )

    assert submission.id == 3
    assert submission.title == "提交測試"
    assert submission.description == "這是一個提交測試"
    assert submission.round_id == 7
    assert submission.is_valid is True
    assert submission.difficulty == DifficultyEnum.medium
    assert submission.status == StatusEnum.success


def test_challenge_submission_response_default_values():
    submission = ChallengeTeamSubmissionResponse(
        id=4,
        title="預設狀態測試",
        description="狀態測試",
        round_id=9,
        is_valid=False
    )

    assert submission.difficulty == DifficultyEnum.easy  # 預設值
    assert submission.status == StatusEnum.doing  # 預設值


def test_challenge_submission_response_validation_error():
    with pytest.raises(ValidationError):
        ChallengeTeamSubmissionResponse(
            id=5,
            title="錯誤測試",
            description="這應該失敗",
            round_id="not_an_int",  # round_id 應該是 int
            is_valid=True
        )
