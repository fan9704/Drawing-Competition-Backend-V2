from src.models.tortoise import Challenge, Round
from src.models.enums import DifficultyEnum


async def get_testcase_challenge_one(round_instance: Round):
    return await Challenge.create(
        id=1,
        title="題目一 苦力怕",
        description="嘶嘶苦力怕",
        difficulty=DifficultyEnum.easy,
        round=round_instance,
        is_valid=True
    )


async def get_testcase_challenge_two(round_instance: Round):
    return await Challenge.create(
        id=2,
        title="題目二 小石",
        description="小石不是折壞的 Macbook",
        difficulty=DifficultyEnum.easy,
        round=round_instance,
        is_valid=True
    )
