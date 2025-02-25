from pydantic import BaseModel, Field


class ClipValidationRequest(BaseModel):
    image1_path: str = Field(default="/images/default.png", examples=["/images/default.png"])
    image2_path: str = Field(default="/images/default.png", examples=["/images/default.png"])


class ClipValidationResponse(BaseModel):
    similarity: float = Field(default=0.0, examples=[11.0], ge=0.0, le=100)
