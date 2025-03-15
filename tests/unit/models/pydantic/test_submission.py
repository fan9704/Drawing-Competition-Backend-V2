import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from src.models.enums import StatusEnum
from src.models.pydantic.submission import (
    Submission,
    SubmissionOneLayer,
    SubmissionStoreJudgeRequest,
    SubmissionStoreJudgeResponse,
    SubmissionSubmitCodeRequest,
    SubmissionSubmitCodeResponse,
    SubmissionTeamRecordResponse,
)
from src.models.pydantic.team import TeamPydantic
from src.models.pydantic.challenge import ChallengePydantic
from src.models.pydantic.round import RoundPydantic


# ✅ 測試 Submission Model 正常建立
def test_create_submission():
    submission_instance = Submission(
        id=1,
        code="print('Hello, World!')",
        status=StatusEnum.todo,
        score=50,
        fitness=80,
        word_count=10,
        execute_time=timedelta(seconds=2),
        stdout="Hello, World!",
        stderr="",
        team=TeamPydantic(id=1, name="第1小隊"),
        time=datetime.now(),
        challenge=ChallengePydantic(id=1, title="題目", description="題目描述", is_valid=True),
        round=RoundPydantic(id=1, start_time=datetime.now(), end_time=datetime.now(), is_valid=True),
        draw_image_url="/images/default.png",
    )

    assert submission_instance.id == 1
    assert submission_instance.score == 50
    assert submission_instance.stdout == "Hello, World!"


# ❌ 測試 Submission Model 驗證錯誤（score 超過範圍）
@pytest.mark.parametrize("invalid_score", [-10, 120])
def test_submission_score_validation_error(invalid_score):
    with pytest.raises(ValidationError):
        Submission(
            id=1,
            code="print('Hello, World!')",
            status=StatusEnum.todo,
            score=invalid_score,  # 錯誤值
            fitness=80,
            word_count=10,
            execute_time=timedelta(seconds=2),
            stdout="Hello, World!",
            stderr="",
            team=TeamPydantic(id=1, name="第1小隊"),
            time=datetime.now(),
            challenge=ChallengePydantic(id=1, title="題目", description="題目描述", is_valid=True),
            round=RoundPydantic(id=1, start_time=datetime.now(), end_time=datetime.now(), is_valid=True),
        )


# ✅ 測試 SubmissionOneLayer Model 正常建立
def test_create_submission_one_layer():
    submission_instance = SubmissionOneLayer(
        id=2,
        code="x = 1 + 2",
        status=StatusEnum.todo,
        score=30,
        fitness=70,
        word_count=15,
        execute_time=timedelta(seconds=1),
        stdout="3",
        stderr="",
        team=1,
        time=datetime.now(),
        challenge=2,
        round=1,
    )

    assert submission_instance.id == 2
    assert submission_instance.score == 30
    assert submission_instance.team == 1


# ✅ 測試 SubmissionStoreJudgeRequest Model 正常建立
def test_create_submission_store_judge_request():
    judge_request = SubmissionStoreJudgeRequest(
        score=80,
        fitness=90,
        word_count=25,
        execution_time=3,
        stdout="Execution Success",
        stderr="",
        status=StatusEnum.doing,
    )

    assert judge_request.score == 80
    assert judge_request.execution_time == 3


# ❌ 測試 SubmissionStoreJudgeRequest 驗證錯誤（execution_time 為負數）
def test_submission_store_judge_request_invalid_execution_time():
    with pytest.raises(ValidationError):
        SubmissionStoreJudgeRequest(score=80, fitness=90, word_count=25, execution_time=-1, stdout="", stderr="",
                                    status=StatusEnum.doing)


# ✅ 測試 SubmissionStoreJudgeResponse Model 正常建立
def test_create_submission_store_judge_response():
    judge_response = SubmissionStoreJudgeResponse(
        id=5,
        team_id=2,
        score=90,
        code="def add(a, b): return a + b",
        fitness=85,
        word_count=40,
        execution_time=2,
        stdout="5",
        stderr="",
        status=StatusEnum.success,
        draw_image_url="/images/result.png",
        time=datetime.now(),
        challenge_id=3,
        round_id=1,
    )

    assert judge_response.id == 5
    assert judge_response.team_id == 2
    assert judge_response.execution_time == 2


# ✅ 測試 SubmissionSubmitCodeRequest Model 正常建立
def test_create_submission_submit_code_request():
    submit_request = SubmissionSubmitCodeRequest(code="x = 5", team=1, challenge=3)

    assert submit_request.code == "x = 5"
    assert submit_request.team == 1


# ✅ 測試 SubmissionSubmitCodeResponse Model 正常建立
def test_create_submission_submit_code_response():
    submit_response = SubmissionSubmitCodeResponse(
        challenge=3,
        code="print('Test')",
        draw_image_url="/images/code.png",
        round=1,
        status=StatusEnum.doing,
        team=2,
        time=datetime.now(),
    )

    assert submit_response.challenge == 3
    assert submit_response.status == StatusEnum.doing


# ✅ 測試 SubmissionTeamRecordResponse Model 正常建立
def test_create_submission_team_record_response():
    team_record = SubmissionTeamRecordResponse(
        id=10,
        team_id=3,
        stderr="",
        challenge_id=5,
        round_id=2,
        status=StatusEnum.success,
        code="print('Hello')",
        execute_time=timedelta(seconds=4),
        score=95,
        stdout="Hello",
        draw_image_url="/images/output.png",
        fitness=99,
        time=datetime.now(),
        word_count=35,
    )

    assert team_record.id == 10
    assert team_record.status == StatusEnum.success
    assert team_record.fitness == 99
    assert team_record.stdout == "Hello"
