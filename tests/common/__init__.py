from tests.common.logger import setup_test_logger
# import pytest
# from tortoise import Tortoise
# from src.configs import tortoise_config
#
# @pytest.fixture()
# async def init_db():
#     """
#     初始化 Tortoise ORM (基於原始 `init_db` 設定)
#     """
#     config = {
#         "use_tz": True,
#         "timezone": "Asia/Taipei",
#         "connections": {
#             "default": tortoise_config.db_url
#         },
#         "apps": {
#             "models": {
#                 "models": ["src.models.tortoise"],
#                 'default_connection': 'default',
#             }
#         }
#     }
#
#     # 手動初始化 Tortoise ORM
#     await Tortoise.init(config=config)
#     await Tortoise.generate_schemas()  # 建立表格
#     yield
#     await Tortoise.close_connections()  # 測試結束後關閉資料庫