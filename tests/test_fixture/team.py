from src.models.tortoise import Team


async def get_testcase_team_one():
    return await Team.create(
        id=1,
        name="第1小隊",
        token="ABCD"
    )


async def get_testcase_team_two():
    return await Team.create(
        id=2,
        name="第2小隊",
        token="5678"
    )
