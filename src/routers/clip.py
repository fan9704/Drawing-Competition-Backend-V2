from fastapi import APIRouter

from src.utils.clip import Clip
from src.models.pydantic import ClipValidationRequest, ClipValidationResponse

router = APIRouter()

@router.post("/",
             summary="Validation Image",
             description="Validation Image",
             response_model=ClipValidationResponse)
async def clip(request:ClipValidationRequest):
    clip_instance = Clip().get_instance()
    similarity = clip_instance.calculate_similarity(request.image1_path,request.image2_path)
    return ClipValidationResponse(similarity=similarity)