from typing import Optional, List

from fastapi import APIRouter, Response

from src.models.pydantic import Team, TeamAuthRequest, TeamAuthResponse
from src.models.tortoise import Team as ITeam
from src.repositories import TeamRepository
from src.utils import jwt

router = APIRouter()
repository: TeamRepository = TeamRepository(ITeam)


@router.get("/",
            description="Get All Teams",
            response_model=List[Team],
            response_description="All Teams")
async def get() -> list[Team]:
    return await repository.find_all()


@router.get("/{token}",
            description="Get Team by Tokens",
            response_model=Optional[Team],
            response_description="Your Team")
async def get_team_by_token(token: str):
    team = await ITeam.filter(token=token).first()
    if not team:
        return Response(status_code=400, content="Token is invalid")
    return team


@router.post("/auth", response_model=TeamAuthResponse)
async def auth_team(request: TeamAuthRequest):
    team = await ITeam.filter(token=request.token).first()
    status = False
    token = None

    if team:
        token = jwt.create_access_token(team)
    return TeamAuthResponse(
        status=status,
        team=team,
        access_token=token
    )