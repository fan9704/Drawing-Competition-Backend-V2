import asyncio
import json
from src.initializer import init_redis_pool
from typing import List
from fastapi import WebSocket

connected_clients:List[WebSocket] = []

async def leaderboard_listener():
    pub_sub = init_redis_pool().pubsub()
    pub_sub.subscribe('get_all_team_single_round_total_score')

    loop = asyncio.get_event_loop()

    for message in pub_sub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            for client in connected_clients:
                asyncio.run_coroutine_threadsafe(client.send_json(data),loop)