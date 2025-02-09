from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.tortoise import Challenge as IChallenge

ChallengePydantic = pydantic_model_creator(IChallenge, name="Challenge")
ChallengeWithOutRelationPydantic = pydantic_model_creator(IChallenge, exclude=("team", "challenge"), name="ChallengeWithoutRelation")

class Challenge(BaseModel):
    id:int
    title: str
    description: str
    image_url: str
    difficulty: str
    round_id: int
    is_valid: bool

class ChallengeTeamSubmissionResponse(BaseModel):
    id: int
    title: str
    description: str
    round_id: int
    is_valid: bool
    difficulty: str
    status: str