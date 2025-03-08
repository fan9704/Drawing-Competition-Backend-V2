from src.models.tortoise import Round
from datetime import datetime, timedelta


async def get_testcase_round_one():
    return await Round.create(
        id=1,
        start_time=datetime.now() - timedelta(hours=3),
        end_time=datetime.now() + timedelta(hours=3),
        is_valid=True
    )


async def get_testcase_round_two():
    return await Round.create(
        id=2,
        start_time=datetime.now() + timedelta(hours=3),
        end_time=datetime.now() + timedelta(hours=6),
        is_valid=False
    )
