from src.models.pydantic import ChallengePydantic
from src.models.tortoise import Submission
from src.repositories.base import Repository
from src.models.tortoise.team import Team
from src.models.tortoise.challenge import Challenge
from src.models.tortoise.round import Round
from tortoise.functions import Max

class SubmissionRepository(Repository):
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

    # 根據是否有 TeamId 取得所有 Submission，並依照 Challenge 和反向 time 排序
    async def find_all_submission_query_by_team_id_order_by_challenge_and_reverse_time(self, team_id: int):
        if team_id is None:
            qs = self.model.all().order_by("challenge", "-time")
        else:
            qs = self.model.filter(team__id=team_id).order_by("challenge", "-time")
        return await qs.all()

    # 過濾傳入的 submissions，根據 Challenge 取得最新一筆 Submission
    async def filter_submission_by_challenge(self, team_id:int, challenge: Challenge):
        return await self.model.filter(team__id=team_id,challenge=challenge).first()

    # 根據 TeamId 取得所有 Submission 的查詢結果
    async def find_all_submission_query_by_team_id(self, team_id: int):
        if team_id is None:
            return await self.model.all()
        else:
            return await self.model.filter(team__id=team_id).all()

    # 過濾傳入的 submissions，取出各 Challenge 的最高分
    async def get_submission_highest_score(self, submissions):
        qs = submissions.annotate(max_score=Max("score")).group_by("challenge")
        return await qs.values("challenge", "max_score")

    # 過濾傳入的 submissions，根據 Round 與 Team 取出各 Challenge 的最高分
    async def get_submission_highest_score_by_round_and_team(self, submissions, round_obj: Round, team: Team):
        qs = submissions.filter(round=round_obj, team=team).annotate(max_score=Max("score")).group_by("challenge")
        return await qs.values("challenge", "max_score")

    # 過濾傳入的 submissions，取出各 Challenge 的最高分，並回傳 Team、fitness、execute_time 與 word_count 等資訊
    async def get_submission_highest_score_with_full_record(self, submissions):
        qs = submissions.annotate(max_score=Max("score")).group_by("team").order_by("-max_score")
        return await qs.values("team", "fitness", "execute_time", "max_score", "word_count")

    # 過濾傳入的 submissions，根據 Challenge 與 Score 取出一筆 Submission
    async def filter_submission_by_challenge_and_score(self, submissions, challenge, score):
        return await submissions.filter(challenge=challenge, score=score).first()

    # 計算傳入 submissions 中，根據 TeamId 與 Challenge 過濾後的 Submission 個數
    async def count_submission_query_by_team_id_filter_by_challenge(self, submissions, team_id: int, challenge: Challenge):
        if team_id is None:
            return await submissions.filter(challenge=challenge).count()
        else:
            return await submissions.filter(challenge=challenge, team_id=team_id).count()

    # 取得 Submission 根據 TeamId 與 RoundId 的查詢結果
    async def find_all_submission_query_by_team_id_and_filter_by_round_id(self, team_id: int, round_id: int):
        if team_id is None:
            qs = self.model.filter(round__id=round_id)
        else:
            qs = self.model.filter(team_id=team_id, round__id=round_id)
        return await qs.all()

    # 建立暫時性的 Submission
    async def create_temperate_submission(self, code:str,team_id:int,challenge_id:int):
        challenge = await Challenge.get(id=challenge_id).prefetch_related("round")
        submission = await self.model.create(
            code = code,
            status="doing",
            team_id = team_id,
            challenge_id = challenge_id,
            round_id=challenge.round.id,
        )
        await submission.save()
        return submission