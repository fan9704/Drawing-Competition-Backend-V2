import os
import secrets
import string
import typer
import pytz
from tortoise.transactions import in_transaction

from src.models.tortoise import Team, Round
from datetime import datetime, date, timedelta
from tortoise import Tortoise, run_async
from dotenv import load_dotenv

load_dotenv()
app = typer.Typer()
tz = pytz.timezone('Asia/Taipei')

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")

POSTGRES_DB_URL = f'postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'

async def init_db():
    """初始化 Tortoise ORM"""
    await Tortoise.init(
        db_url=POSTGRES_DB_URL,
        modules={"models": ["src.models.tortoise"]},
    )
    await Tortoise.generate_schemas()


@app.command("create_teams")
def create_teams():
    """建立 10 個小隊並生成對應的 token"""
    def generate_token():
        return ''.join(secrets.choice(string.ascii_letters + string.digits).upper() for _ in range(4))

    async def _create_team():
        await init_db()
        for i in range(1, 11):
            team, _ = await Team.get_or_create(pk=i)
            team.token = generate_token()
            team.name = f"第{i}小隊"
            await team.save()

            # team = await Team.create(name=f"第{i}小隊", token=generate_token())
            typer.echo(f"✅ 成功建立小隊: {team.name} (Token: {team.token})")
        await Tortoise.close_connections()

    run_async(_create_team())


@app.command("create_rounds")
def create_rounds():
    """
    建立 5 個回合，並自動計算開始/結束時間以及間隔
    """
    ROUND_START_HOUR = 14  # 回合開始時間-小時
    ROUND_START_MINUTE = 0  # 回合開始時間-分鐘
    ROUND_PLAY_TIME = 30  # 回合時間長度-分鐘
    ROUND_GAP_TIME = 10  # 回合間隔時間-分鐘

    async def _create_rounds():
        await init_db()
        start_time = None
        end_time = None
        async with in_transaction():  # 保持交易一致性
            for i in range(1, 6):
                if i == 1:
                    start_time = datetime.combine(
                        date=date.today(),
                        time=datetime.min.time().replace(
                            hour=ROUND_START_HOUR, minute=ROUND_START_MINUTE
                        ),
                    )
                    start_time = tz.localize(start_time)  # 設定時區
                    end_time = start_time + timedelta(minutes=ROUND_PLAY_TIME)
                else:
                    start_time = end_time + timedelta(minutes=ROUND_GAP_TIME)
                    end_time = start_time + timedelta(minutes=ROUND_PLAY_TIME)
                round_instance, _ = await Round.get_or_create(pk=i)
                round_instance.start_time = start_time
                round_instance.end_time = end_time
                round_instance.is_valid = False
                await round_instance.save()

                typer.echo(
                    f"✅ 成功建立回合 {round_instance.id} - 開始: {round_instance.start_time} 結束: {round_instance.end_time}")

    import asyncio
    asyncio.run(_create_rounds())


if __name__ == "__main__":
    app()
