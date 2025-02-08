from tortoise.functions import Max

from src.models.pydantic import SubmissionOneLayerPydantic
from src.models.pydantic.statistic import StatisticTeamChallengeScoreResponseDTO, \
    StatisticTeamChallengeSubmissionCountResponseDTO, StatisticTeamRoundTotalScoreResponseDTO, \
    StatisticAllTeamSingleRoundTotalScoreResponseDTO, StatisticTop3TeamChallengeScoreResponseDTO, \
    StatisticAllTeamRoundTotalScoreResponseDTO
from src.models.tortoise import Submission
from src.models.tortoise.challenge import Challenge as IChallenge
from src.models.tortoise.round import Round as IRound
from src.models.tortoise.team import Team as ITeam
from src.repositories.challenge import ChallengeRepository
from src.repositories.base import Repository
from src.repositories.team import TeamRepository

challenge_repository:ChallengeRepository = ChallengeRepository(IChallenge)
team_repository:TeamRepository = TeamRepository(ITeam)

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
    async def filter_submission_by_challenge(self, team_id:int, challenge: IChallenge):
        return await self.model.filter(team__id=team_id,challenge=challenge).first()

    # 計算該 Team ID 每個挑戰的最高分
    async def find_all_highest_submission_by_team_id(self, team_id: int):
        qs = []
        for challenge in await challenge_repository.find_all():
            max_score_submission = await self.model.filter(
                team__id=team_id,
                challenge=challenge
            ).order_by("-score").first()
            max_score = await self.model.filter(team__id=team_id,challenge=challenge).order_by("-score").first().values()
            res = StatisticTeamChallengeScoreResponseDTO(
                challenge=challenge.id,
                team_id=team_id,
                max_score=max_score["score"],
                submission=await SubmissionOneLayerPydantic.from_tortoise_orm(max_score_submission),
            )
            qs.append(res)
        return qs

    # 計算該 Team Id 提交每個挑戰次數
    async def count_team_all_count_submission(self,team_id:int):
        qs = []
        for challenge in await challenge_repository.find_all():
            submission_count = await self.model.filter(team__id=team_id,challenge=challenge).count()
            res = StatisticTeamChallengeSubmissionCountResponseDTO(
                challenge=challenge.id,
                submission_count=submission_count,
            )
            qs.append(res)
        return  qs

    # 計算該 Team Id 該 Round Id 獲得總分
    async def get_team_round_total_score(self,team_id:int,round_id:int):
        total_score = 0
        for challenge in await challenge_repository.filter(round__id=round_id):
            max_score = await self.model.filter(team__id=team_id,challenge=challenge).order_by("-score").first().values()
            total_score += max_score["score"]
        return StatisticTeamRoundTotalScoreResponseDTO(
            round_id=round_id,
            team_id=team_id,
            total_score=total_score
        )

    # 計算所有 Team 在所有 Round 的分數
    async def get_team_all_challenge_score(self,round_id:int):
        qs = []
        for team in await team_repository.find_all():
            score_list = []
            for challenge in await challenge_repository.filter(round__id=round_id):
                max_score = await self.model.filter(team__id=team.id, challenge=challenge).order_by(
                    "-score").first().values()
                if max_score is None:
                    score_list.append(0)
                else:
                    score_list.append(max_score["score"])
            qs.append(StatisticAllTeamSingleRoundTotalScoreResponseDTO(
                team_id=team.id,
                team_name=team.name,
                total_score=sum(score_list),
                score_list=score_list,
            ))
        return qs

    # 根據 Challenge ID 取得前三高的 Team
    async def get_top3_challenge_score_by_team_id(self,challenge_id:int):
        qs = []
        team_list = set()
        challenge = await challenge_repository.get_by_id(challenge_id)
        for submission in await self.model.filter(challenge=challenge).prefetch_related("team").order_by("-score").values():
            if len(team_list) == 3:
                break
            elif submission["team_id"] in team_list:
                continue
            team = await ITeam.filter(pk=submission["team_id"]).first().values()
            qs.append(StatisticTop3TeamChallengeScoreResponseDTO(
                team=submission["team_id"],
                team_name=team["name"],
                max_score=submission["score"],
                fitness=submission["fitness"],
                execute_time=submission["execute_time"],
                word_count=submission["word_count"],
            ))
            team_list.add(submission["team_id"])
        return qs
    # 取得每個 Round 的 Team Challenge 總分
    async def get_all_round_team_total_challenge_score(self):
        qs = []

        for team in await ITeam.all().values():
            team_id = team["id"]
            team_name = team["name"]
            round_id_list =[]
            total_score_list = []
            for round in await IRound.all().values():
                round_id = round["id"]
                total_score = 0
                for challenge in await challenge_repository.filter(round__id=round_id):
                    max_score = await self.model.filter(team__id=team_id, challenge=challenge).order_by(
                        "-score").first().values()
                    if max_score is not None:
                        total_score += max_score["score"]
                total_score_list.append(total_score)
                round_id_list.append(round_id)
            qs.append(
                StatisticAllTeamRoundTotalScoreResponseDTO(
                    team_id=team_id,
                    team_name=team_name,
                    round_id_list=round_id_list,
                    total_score_list=total_score_list,
                )
            )
        return qs

    # 取得該 Team Id 該 Challenge ID 所有的 status=success 的提交紀錄
    async def find_all_success_submission_by_challenge_id_and_team_id(self,challenge_id:int,team_id:int):
        return await self.model.filter(challenge_id=challenge_id, team_id=team_id,status="success").values()

    # 取得該 Challenge Id 所有 Team 所有 status=success 的提交紀錄
    async def find_all_team_success_submission_challenge_id(self,challenge_id:int):
        return await self.model.filter(challenge_id=challenge_id, status="success").order_by("team_id").values()

    # 列出各題目精選圖片
    async def find_all_challenge_featured_submission(self):
        qs = []
        for challenge in await challenge_repository.find_all():
            submissions = await self.model.filter(challenge=challenge,status="success",score__gt=90).order_by("-score")
            qs.append(
                {
                    "challenge": challenge,
                    "submission": submissions,
                }
            )
        return qs

    # 根據 TeamId 取得所有 Submission 的查詢結果
    async def find_all_submission_query_by_team_id(self, team_id: int):
        if team_id is None:
            return await self.model.filter()
        else:
            return await self.model.filter(team__id=team_id)

    # 過濾傳入的 submissions，取出各 Challenge 的最高分
    async def get_submission_highest_score(self, submissions):
        qs = submissions.annotate(max_score=Max("score")).group_by("challenge")
        return await qs.values("challenge", "max_score")

    # 過濾傳入的 submissions，根據 Round 與 Team 取出各 Challenge 的最高分
    async def get_submission_highest_score_by_round_and_team(self, submissions, round_obj: IRound, team: ITeam):
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
    async def count_submission_query_by_team_id_filter_by_challenge(self, submissions, team_id: int, challenge: IChallenge):
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
        challenge = await IChallenge.get(id=challenge_id).prefetch_related("round")
        submission = await self.model.create(
            code = code,
            status="doing",
            team_id = team_id,
            challenge_id = challenge_id,
            round_id=challenge.round.id,
        )
        await submission.save()
        return submission