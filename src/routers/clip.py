from fastapi import APIRouter, Depends

from src.utils.clip import Clip
from src.dependencies import get_clip_instance
from src.models.pydantic import ClipValidationRequest, ClipValidationResponse

router = APIRouter()


@router.post("/",
             summary="辨識圖片",
             description="Validation Image",
             response_model=ClipValidationResponse,
             response_description="Validation Image Similarity",
             )
async def clip(request: ClipValidationRequest,
               clip_instance: Clip = Depends(get_clip_instance)) -> ClipValidationResponse:
    similarity = clip_instance.calculate_clip_similarity(request.image1_path, request.image2_path)
    return ClipValidationResponse(similarity=similarity)
