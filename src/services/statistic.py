from typing import List

from src.models.pydantic import SubmissionOneLayerPydantic
from src.models.pydantic.statistic import StatisticTeamChallengeScoreResponseDTO, \
    StatisticTeamChallengeSubmissionCountResponseDTO, StatisticTeamRoundTotalScoreResponseDTO, \
    StatisticAllTeamSingleRoundTotalScoreResponseDTO, StatisticTop3TeamChallengeScoreResponseDTO, \
    StatisticAllTeamRoundTotalScoreResponseDTO
from src.repositories.submission import SubmissionRepository
from src.repositories.team import TeamRepository
from src.repositories.challenge import ChallengeRepository
from src.repositories.round import RoundRepository
from src.dependencies.repositories import get_submission_repository, get_challenge_repository, get_team_repository, \
    get_round_repository



class StatisticService:
    def __init__(self,
                repository:SubmissionRepository = get_submission_repository(),
                challenge_repository: ChallengeRepository = get_challenge_repository(),
                team_repository: TeamRepository = get_team_repository(),
                round_repository: RoundRepository = get_round_repository(),
    ):
        self.repository = repository
        self.challenge_repository = challenge_repository
        self.team_repository = team_repository
        self.round_repository = round_repository


    # 根據是否有 TeamId 取得所有 Submission，並依照 Challenge 和反向 time 排序
    async def find_all_submission_query_by_team_id_order_by_challenge_and_reverse_time(self,team_id: int):
        if team_id is None:
            return await self.repository.find_all_submission_order_by_challenge_and_reverse_time()
        else:
            return await self.repository.find_all_submission_query_by_team_id_order_by_challenge_and_reverse_time(team_id)

    # 計算該 Team Id 提交每個挑戰次數
    async def count_team_all_count_submission(self,team_id: int) -> List[
        StatisticTeamChallengeSubmissionCountResponseDTO]:
        qs = []
        for challenge in await self.challenge_repository.find_all():
            submission_count = await self.repository.count_submission_by_team_id_and_challenge_id(
                team_id=team_id,
                challenge_id=challenge.id
            )
            res = StatisticTeamChallengeSubmissionCountResponseDTO(
                challenge=challenge.id,
                submission_count=submission_count
            )
            qs.append(res)
        return qs


    # 計算該 Team ID 每個挑戰的最高分
    async def find_all_highest_submission_by_team_id(self,team_id: int):
        qs = []
        for challenge in await self.challenge_repository.find_all():
            max_score_submission = await self.repository.find_max_score_submission_by_challenge_id_and_team_id(
                team_id=team_id,
                challenge_id=challenge.id
            )
            max_score = await self.repository.get_submission_highest_score_by_team_and_challenge(team_id, challenge.id)
            if max_score is None:
                continue
            else:
                max_score = max_score["score"]
            submission = await SubmissionOneLayerPydantic.from_tortoise_orm(max_score_submission)
            res = StatisticTeamChallengeScoreResponseDTO(
                challenge=challenge.id,
                team_id=team_id,
                max_score=max_score,
                submission=submission,
            )
            qs.append(res)
        return qs




    # 計算該 Team Id 該 Round Id 獲得總分
    async def get_team_by_team_id_round_total_score(self,team_id: int, round_id: int) -> StatisticTeamRoundTotalScoreResponseDTO:
        total_score = 0
        for challenge in await self.challenge_repository.filter(round__id=round_id):
            max_score = await self.repository.get_submission_highest_score_by_team_and_challenge(
                team_id=team_id,
                challenge_id=challenge.id
            )
            if max_score is None:
                break
            else:
                total_score += max_score["score"]
        return StatisticTeamRoundTotalScoreResponseDTO(
            round_id=round_id,
            team_id=team_id,
            total_score=total_score
        )


    # 計算所有 Team 在所有 Round 的分數
    async def get_team_all_challenge_score(self,round_id: int):
        qs = []
        for team in await self.team_repository.find_all():
            score_list = []
            for challenge in await self.challenge_repository.filter(round__id=round_id):
                max_score = await self.repository.get_submission_highest_score_by_team_and_challenge(
                    team_id=team.id,
                    challenge_id=challenge.id
                )
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
    async def get_top3_challenge_score_by_team_id(self,challenge_id: int):
        qs = []
        team_list = set()
        for submission in await self.repository.find_all_submission_by_challenge_id_prefetch_team_desc_order_by_score(
                challenge_id):
            if len(team_list) == 3:
                break
            elif submission["team_id"] in team_list:
                continue
            team = await self.team_repository.get_by_id(pk=submission["team_id"])
            qs.append(StatisticTop3TeamChallengeScoreResponseDTO(
                team=submission["team_id"],
                team_name=team.name,
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

        for team in await self.team_repository.find_all():
            team_id = team.id
            team_name = team.name
            round_id_list = []
            total_score_list = []
            for round_instance in await self.round_repository.find_all():
                round_id = round_instance.id
                total_score = 0
                for challenge in await self.challenge_repository.filter(round__id=round_id):
                    max_score = await self.repository.get_submission_highest_score_by_team_and_challenge(
                        team_id=team_id,
                        challenge_id=challenge.id
                    )
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


    # 列出各題目精選圖片
    async def find_all_challenge_featured_submission(self):
        qs = []
        for challenge in await self.challenge_repository.find_all():
            submissions = await self.repository.find_all_more_90_submission_by_challenge_id_and_success_desc_order_by_score(
                challenge_id=challenge.id
            )
            qs.append(
                {
                    "challenge": challenge,
                    "submission": submissions,
                }
            )
        return qs