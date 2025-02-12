import datetime
import os
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from src.configs.cfg import DRAWING_TEMPLATE_PATH, MAIN_DRAWING_PATH
from src.models.pydantic import SubmissionStoreJudgeRequest
from src.models.pydantic.submission import SubmissionSubmitCodeRequest, SubmissionSubmitCodeResponse, \
    SubmissionTeamRecordResponse, SubmissionOneLayerPydantic, SubmissionStoreJudgeResponse
from src.models.tortoise import Submission as ISubmission
from src.repositories import ChallengeRepository
from src.repositories import SubmissionRepository
from src.utils.judge import judge_submission

router = APIRouter()

# Repository 依賴
def get_challenge_repository() -> ChallengeRepository:
    return ChallengeRepository()

def get_submission_repository() -> SubmissionRepository:
    return SubmissionRepository()


# Store API - 更新 Submission
@router.post("/store/{pk}/",
             summary="儲存提交",
             description="Store submission",
             response_model=SubmissionStoreJudgeResponse,
             response_description="Score store full submission record"
)
async def store_submission(pk: int, data: SubmissionStoreJudgeRequest,
                           repository: SubmissionRepository= Depends(get_submission_repository),):
    submission = await repository.get_by_id(pk)
    submission.score = data.score
    submission.fitness = data.fitness
    submission.word_count = data.word_count
    submission.execute_time = datetime.timedelta(seconds=data.execution_time)
    submission.stdout = data.stdout
    submission.stderr = data.stderr
    submission.status = data.status
    submission.draw_image_url = f"/media/result/{submission.challenge_id}/team_{submission.team_id}/{pk}.png"
    await repository.save(submission)
    return submission



# Submission API - 提交程式碼
@router.post("/",
             summary="提交程式碼",
             description="Submit code",
             response_model=SubmissionSubmitCodeResponse,
             response_description="Score store full submission record")
async def submit_code(request: SubmissionSubmitCodeRequest,repository: SubmissionRepository= Depends(get_submission_repository),challenge_repository: ChallengeRepository = Depends(get_challenge_repository)):
    # 取得需要的資料
    now = datetime.datetime.now()
    challenge_id =request.challenge
    team_id = request.team
    code = request.code
    challenge = await challenge_repository.get_by_id(challenge_id)
    round_id = await challenge_repository.get_round_by_challenge_id(challenge_id)

    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    last_submission = await repository.find_newest_submission_by_team_id(team_id)
    if last_submission is not None:
        # 計算提交時間差
        diff_time = now.timestamp() - last_submission.time.timestamp()
        if diff_time < 5:
            raise HTTPException(status_code=429, detail="Submission too fast")
    # 開始進行 Judge 前處理
    submission = await repository.create_temperate_submission(
        code=code,
        team_id=team_id,
        challenge_id=challenge_id,
    )
    submission_id = submission.id

    # 各種路徑初始化
    image_url = challenge.image_url
    drawing_template_path = DRAWING_TEMPLATE_PATH
    main_drawing_path = MAIN_DRAWING_PATH
    template_revise_path = f"media/code/{challenge_id}/team_{team_id}/drawing_{submission_id}.py"
    code_path = f"media/code/{challenge_id}/team_{team_id}/submission_{submission_id}.py"
    result_path = f"media/result/{challenge_id}/team_{team_id}/{submission_id}.png"

    # 確保資料夾位址可用
    os.makedirs(os.path.dirname(code_path), exist_ok=True) # 建立程式碼放置路徑
    os.makedirs(os.path.dirname(result_path), exist_ok=True) # 建立圖片放置路徑
    # 寫入程式碼
    with open(code_path, "w") as f:
        f.write(code)

    # 開始 Judge
    judge_submission(
        code_path, # 提交程式碼位址
        image_url, # 挑戰圖片位址
        result_path, # 生成圖片位址
        team_id, # 小隊 ID
        drawing_template_path, # 繪圖 Template 位址
        main_drawing_path, # 評判分數檔案
        template_revise_path,# 修改後 Template 位址
        submission_id, # 提交 Submission ID
    )

    response = {
        "challenge": challenge_id,
        "code": code,
        "draw_image_url": result_path,
        "round": round_id,
        "status": "success",
        "team": team_id,
        "time": submission.time,
    }
    await submission.save()
    return response


# Get all submissions by team and challenge
@router.get("/all/{challenge_id}/{team_id}/",
            summary="取得該 Team 所有提交 ",
            description="Get all submissions by team id",
            response_model=List[SubmissionTeamRecordResponse],
            response_description="All submission records by team id"
            )
async def get_submissions_by_team_and_challenge(challenge_id: int, team_id: int):
    submissions = await ISubmission.filter(challenge_id=challenge_id, team_id=team_id).order_by("-time")
    return submissions


# Get the highest score submission by team and challenge
# TODO: Change Route
@router.get("/max/{challenge_id}/{team_id}/",
            summary="取得該 Team 於 Challenge最高分",
            description="Get Highest Score in challenge id and team id",
            response_model=SubmissionOneLayerPydantic,
            response_description="Highest Score in that team"
)
async def get_highest_score_submission(challenge_id: int, team_id: int,repository: SubmissionRepository = Depends(get_submission_repository)):
    submission = await repository.find_max_score_submission_by_challenge_id_and_team_id(challenge_id, team_id)
    if not submission:
        raise HTTPException(status_code=404, detail="No submission found")
    return submission


# Get all submissions by team
@router.get("/team/{team_id}/",
            summary="取得該 Team 所有提交",
            description="Get team all submission",
            response_model=List[SubmissionOneLayerPydantic],
            response_description="Get All submission by team id"
)
async def get_all_submissions_by_team(team_id: int,repository: SubmissionRepository = Depends(get_submission_repository)):
    submissions = await repository.find_all_submission_by_team_id(team_id)
    return submissions