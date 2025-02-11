import json
from typing import List

from fastapi import WebSocket, Depends, APIRouter
from redis import Redis

from src.initializer import init_redis_pool
from src.main import app

connected_clients:List[WebSocket] = []
LEADERBOARD_KEY = "leaderboard"
router = APIRouter()


@app.websocket('/ws/statistic')
async def ws_get_all_team_single_round_total_score(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.send_text(str(len(connected_clients)))
    except:
        connected_clients.remove(websocket)

@router.post("/update_score/team/{team_id}/")
async def update_score_team(team_id:int,score:int,redis_client:Redis = Depends(init_redis_pool)):
    await redis_client.zadd(LEADERBOARD_KEY, {str(team_id): score})
    leaderboard = await get_leaderboard()
    await redis_client.publish("get_all_team_single_round_total_score", json.dumps(leaderboard))
    return {
        "message":"Score updated",
        "leaderboard":leaderboard
    }

async def get_leaderboard():
    redis_client = init_redis_pool()
    top_players = await redis_client.zrevrange(LEADERBOARD_KEY, 0, 9, withscores=True)
    return [{"team_id":int(team_id),"score":score} for team_id,score in top_players]
