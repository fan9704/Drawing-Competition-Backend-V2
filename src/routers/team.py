from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from src.models.pydantic import Team, TeamAuthRequest, TeamAuthResponse
from src.repositories import TeamRepository
from src.dependencies import get_team_repository
from src.utils import jwt

router = APIRouter()


@router.get("/",
            summary="取得所有 Team",
            description="Get All Teams",
            response_model=List[Team],
            response_description="All Teams")
async def get(repository: TeamRepository = Depends(get_team_repository)) -> List[Team]:
    return await repository.find_all()


@router.get("/{token}/",
            summary="認證 Team 透過 Token",
            description="Get Team by Tokens",
            response_model=Optional[Team],
            response_description="Your Team")
async def get_team_by_token(token: str, repository: TeamRepository = Depends(get_team_repository)) -> Optional[Team]:
    team = await repository.get_team_by_token(token=token)
    if not team:
        raise HTTPException(status_code=400, detail="Token is invalid")
    return team


@router.post("/auth/token/",
             summary="認證 Team 透過 Token 並取得 JWT",
             description="Team Auth with Token API",
             response_model=TeamAuthResponse,
             response_description="Your Team Information")
async def auth_team(request: TeamAuthRequest,
                    repository: TeamRepository = Depends(get_team_repository)) -> TeamAuthResponse:
    team = await repository.get_team_by_token(token=request.token)
    status = False
    token = None

    if team:
        token = jwt.create_team_access_token(team)
        status = True
    return TeamAuthResponse(
        status=status,
        team=team,
        access_token=token
    )
