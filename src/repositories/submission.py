from tortoise.functions import Max

from src.models.tortoise import Submission
from src.models.tortoise.challenge import Challenge as IChallenge
from src.models.tortoise.round import Round as IRound
from src.models.tortoise.submission import Submission as ISubmission
from src.models.tortoise.team import Team as ITeam
from src.repositories.base import Repository
from src.repositories.challenge import ChallengeRepository
from src.repositories.team import TeamRepository

challenge_repository: ChallengeRepository = ChallengeRepository()
team_repository: TeamRepository = TeamRepository()


class SubmissionRepository(Repository):
    def __init__(self):
        self.model = ISubmission

    # 取得最新一筆 Submission（依據 id 遞增假設最新者 id 最大）
    async def get_last_submission(self):
        return await self.model.all().order_by("-id").first()

    # 取得該 Team 最新一筆 Submission（以 time 欄位排序取第一筆）
    async def find_newest_submission_by_team_id(self, team_id: int) -> Submission | None:
        return await self.model.filter(team__id=team_id).order_by("-time").first()

    # 取得該 Team & Challenge 依照時間排序的所有 Submission（時間遞減）
    async def find_all_submission_by_challenge_id_and_team_id(self, challenge_id: int, team_id: int):
        return await self.model.filter(challenge__id=challenge_id, team__id=team_id).order_by("-time").all()

    # 取得該 Team & Challenge 中分數最高的 Submission
    async def find_max_score_submission_by_challenge_id_and_team_id(self, challenge_id: int, team_id: int):
        return await self.model.filter(challenge__id=challenge_id, team__id=team_id).order_by("-score").first()

    # 取得該 Challenge 的所有 Submission
    async def find_all_submission_by_challenge_id(self, challenge_id: int):
        return await self.model.filter(challenge__id=challenge_id).all()

    # 取得該 Team 的所有 Submission
    async def find_all_submission_by_team_id(self, team_id: int):
        return await self.model.filter(team__id=team_id)

    # 根據 TeamId 取得所有 Submission 並依照 Challenge 和反向 time 排序
    async def find_all_submission_query_by_team_id_order_by_challenge_and_reverse_time(self, team_id: int):
        return self.model.filter(team__id=team_id).order_by("challenge", "-time")

    # 取得所有 Submission 並依照 Challenge 和反向 time 排序
    async def find_all_submission_order_by_challenge_and_reverse_time(self):
        return self.model.filter().order_by("challenge", "-time")

    # 取得所有 submissions，根據 challenge_id 且提前擷取 team 資訊並且由高分到低分排序
    async def find_all_submission_by_challenge_id_prefetch_team_desc_order_by_score(self, challenge_id: int):
        return await self.model.filter(challenge__id=challenge_id).prefetch_related("team").order_by(
            "-score").values()

    # 過濾傳入的 submissions，根據 Challenge 取得最新一筆 Submission
    async def filter_submission_by_challenge(self, team_id: int, challenge: IChallenge):
        return await self.model.filter(team__id=team_id, challenge=challenge).first()

    # 取得該 Team Id 該 Challenge ID 所有的 status=success 的提交紀錄
    async def find_all_success_submission_by_challenge_id_and_team_id(self, challenge_id: int, team_id: int):
        return await self.model.filter(challenge_id=challenge_id, team_id=team_id, status="success").values()

    # 取得該 Challenge Id 所有 Team 所有 status=success 的提交紀錄
    async def find_all_team_success_submission_challenge_id(self, challenge_id: int):
        return await self.model.filter(challenge_id=challenge_id, status="success").order_by("team_id").values()

    # 取得精選 Submission 根據 challenge_id 與 status=success 且超過 90 分
    async def find_all_more_90_submission_by_challenge_id_and_success_desc_order_by_score(self, challenge_id: int):
        return await self.model.filter(challenge__id=challenge_id, status="success", score__gt=90).order_by(
            "-score")

    # 根據 TeamId 取得所有 Submission 的查詢結果
    async def find_all_submission_query_by_team_id(self, team_id: int):
        if team_id is None:
            return await self.model.filter()
        else:
            return await self.model.filter(team__id=team_id)

    # 取得根據 team_id 與 challenge_id 最高分 submission
    async def get_submission_highest_score_by_team_and_challenge(self, team_id: int, challenge_id: int):
        return await self.model.filter(team__id=team_id, challenge__id=challenge_id).order_by("-score").first().values()

    # 過濾傳入的 submissions，取出各 Challenge 的最高分，並回傳 Team、fitness、execute_time 與 word_count 等資訊
    async def get_submission_highest_score_with_full_record(self, submissions):
        qs = submissions.annotate(max_score=Max("score")).group_by("team").order_by("-max_score")
        return await qs.values("team", "fitness", "execute_time", "max_score", "word_count")

    # 計算 submission 數量 根據 team_id 與 challenge_id
    async def count_submission_by_team_id_and_challenge_id(self, team_id: int, challenge_id: int):
        return await self.model.filter(
            challenge__id=challenge_id,
            team__id=team_id
        ).count()

    # 取得 Submission 根據 TeamId 與 RoundId 的查詢結果
    async def find_all_submission_query_by_team_id_and_filter_by_round_id(self, team_id: int, round_id: int):
        if team_id is None:
            qs = await self.model.filter(round__id=round_id)
        else:
            qs = await self.model.filter(team_id=team_id, round__id=round_id)
        return qs
