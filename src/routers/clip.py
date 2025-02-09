from fastapi import APIRouter, Depends

from src.utils.clip import Clip
from src.models.pydantic import ClipValidationRequest, ClipValidationResponse

router = APIRouter()

def get_clip_instance():
    return Clip.get_instance()

@router.post("/",
             summary="Validation Image",
             description="Validation Image",
             response_model=ClipValidationResponse)
async def clip(request:ClipValidationRequest,clip_instance:Clip = Depends(get_clip_instance))-> ClipValidationResponse:
    similarity = clip_instance.calculate_clip_similarity(request.image1_path,request.image2_path)
    return ClipValidationResponse(similarity=similarity)