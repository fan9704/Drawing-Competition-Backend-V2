import pytest
from pydantic import ValidationError
from src.models.pydantic import ClipValidationRequest, ClipValidationResponse


# ✅ 測試 ClipValidationRequest Model 正常建立
def test_create_clip_validation_request():
    request_instance = ClipValidationRequest(
        image1_path="/images/test1.png",
        image2_path="/images/test2.png"
    )

    assert request_instance.image1_path == "/images/test1.png"
    assert request_instance.image2_path == "/images/test2.png"


# ✅ 測試 ClipValidationRequest 預設值
def test_clip_validation_request_default_values():
    request_instance = ClipValidationRequest()

    assert request_instance.image1_path == "/images/default.png"
    assert request_instance.image2_path == "/images/default.png"


# ❌ 測試 ClipValidationRequest 驗證錯誤（image1_path 應該是 str）
def test_clip_validation_request_validation_error():
    with pytest.raises(ValidationError):
        ClipValidationRequest(image1_path=123, image2_path=456)  # 錯誤類型


# ✅ 測試 ClipValidationResponse Model 正常建立
def test_create_clip_validation_response():
    response_instance = ClipValidationResponse(similarity=85.5)

    assert response_instance.similarity == 85.5


# ✅ 測試 ClipValidationResponse 預設值
def test_clip_validation_response_default_values():
    response_instance = ClipValidationResponse()

    assert response_instance.similarity == 0.0  # 預設值應該是 0.0


# ❌ 測試 ClipValidationResponse 驗證錯誤（similarity 應該在 0 到 100 之間）
@pytest.mark.parametrize("invalid_value", [-5, 120, "not_a_number"])
def test_clip_validation_response_validation_error(invalid_value):
    with pytest.raises(ValidationError):
        ClipValidationResponse(similarity=invalid_value)
