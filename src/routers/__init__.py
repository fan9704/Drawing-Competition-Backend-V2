from src.routers.items import router as items_router
from src.routers.team import router as teams_router
from src.utils.api import TypedAPIRouter

items_router = TypedAPIRouter(router=items_router, prefix="/items", tags=["item"])
teams_router = TypedAPIRouter(router=teams_router, prefix="/teams", tags=["team"])