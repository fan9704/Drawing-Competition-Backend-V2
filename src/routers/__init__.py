from src.routers.team import router as teams_router
from src.routers.round import router as rounds_router
from src.routers.clip import  router as clip_router
from src.routers.challenge import router as challenge_router
from src.routers.submission import  router as submission_router
from src.routers.statistic import  router as statistic_router
from src.utils.api import TypedAPIRouter

teams_router = TypedAPIRouter(router=teams_router, prefix="/api/team", tags=["team"])
rounds_router = TypedAPIRouter(router=rounds_router, prefix="/api/round", tags=["round"])
clip_router = TypedAPIRouter(router=clip_router, prefix="/api/clip", tags=["clip"])
challenge_router = TypedAPIRouter(router=challenge_router, prefix="/api/challenge", tags=["challenge"])
submission_router = TypedAPIRouter(router=submission_router, prefix="/api/submission", tags=["submission"])
statistic_router = TypedAPIRouter(router=statistic_router, prefix="/api/statistic", tags=["statistic"])