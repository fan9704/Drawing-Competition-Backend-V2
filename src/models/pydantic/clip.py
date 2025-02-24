from pydantic import BaseModel, Field


class ClipValidationRequest(BaseModel):
    image1_path: str = Field(default="/images/default.png")
    image2_path: str = Field(default="/images/default.png")


class ClipValidationResponse(BaseModel):
    similarity: float = Field(examples=[11.0], gt=0.0, lt=100)
