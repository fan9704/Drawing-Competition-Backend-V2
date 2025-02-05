from pydantic import BaseModel

class ClipValidationRequest(BaseModel):
    image1_path: str
    image2_path: str

class ClipValidationResponse(BaseModel):
    similarity: float