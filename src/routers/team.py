from typing import Optional

from fastapi import APIRouter, HTTPException
from src.repositories import TeamRepository
from src.models.tortoise import Team as ITeam
from src.models.pydantic import Team

router = APIRouter()
repository: TeamRepository = TeamRepository(ITeam)


@router.get("/", description="Get All Teams")
async def get() -> list[Team]:
    return await repository.find_all()


@router.get("/{token}", description="Get Team by Tokens", response_model=Optional[Team])
async def get_team_by_token(token: str):
    team = await Team.filter(token=token).first()
    if not team:
        raise HTTPException(status_code=400, detail="Token is invalid")
    return team
