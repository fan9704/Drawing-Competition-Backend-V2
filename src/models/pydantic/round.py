import datetime
from pydantic import BaseModel

class Round(BaseModel):
    start_time:datetime.datetime
    end_time:datetime.datetime
    is_valid:bool

    class Config:
        orm_mode = True

class RoundChallengeResponse(BaseModel):
    id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_valid: bool
