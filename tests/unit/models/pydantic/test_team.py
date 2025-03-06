import pytest
from pydantic import ValidationError
from src.models.pydantic.team import Team, TeamAuthRequest, TeamAuthResponse
from src.models.tortoise import Team as ITeam
from tortoise.contrib.pydantic import pydantic_model_creator

# 產生 Pydantic Model
TeamPydanticWithoutToken = pydantic_model_creator(ITeam, exclude=("token",))


# ✅ 測試 Team Model 正常建立
def test_create_team():
    team_instance = Team(id=1, name="第1小隊")

    assert team_instance.id == 1
    assert team_instance.name == "第1小隊"


# ❌ 測試 Team Model 驗證錯誤（id 應該是 int）
def test_team_validation_error():
    with pytest.raises(ValidationError):
        Team(id="not_an_int", name="第1小隊")  # 錯誤類型


# ✅ 測試 TeamAuthRequest Model 正常建立
def test_create_team_auth_request():
    auth_request = TeamAuthRequest(token="ABCD")

    assert auth_request.token == "ABCD"


# ❌ 測試 TeamAuthRequest 驗證錯誤（token 長度應為 4）
@pytest.mark.parametrize("invalid_token", ["A", "ABCDE", ""])
def test_team_auth_request_validation_error(invalid_token):
    with pytest.raises(ValidationError):
        TeamAuthRequest(token=invalid_token)


# ✅ 測試 TeamAuthResponse Model 正常建立
def test_create_team_auth_response():
    team_data = TeamPydanticWithoutToken(id=2, name="第2小隊")

    auth_response = TeamAuthResponse(status=True, team=team_data, access_token="XYZ123")

    assert auth_response.status is True
    assert auth_response.team.id == 2
    assert auth_response.team.name == "第2小隊"
    assert auth_response.access_token == "XYZ123"


# ✅ 測試 TeamAuthResponse Model 空值
def test_create_team_auth_response_with_null_values():
    auth_response = TeamAuthResponse(status=False, team=None, access_token=None)

    assert auth_response.status is False
    assert auth_response.team is None
    assert auth_response.access_token is None
