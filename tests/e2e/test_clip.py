import pytest

from src.models.tortoise import Team
from tests.test_fixture import get_testcase_team_one, get_testcase_team_two


# class TestE2EClip:
#     @pytest.mark.asyncio
#     async def test_clip(self, http_client, in_memory_db):
#         data = {
#             "image1_path": "/media/images/1.png",
#             "image2_path": "/media/images/1_test_outcome.png"
#         }
#
#         response = await http_client.post(
#             url="/api/clip/",
#             json=data
#         )
#         print(f"Response: {response.text}")
#
#         assert response.status_code == 200
#         assert response.json()["similarity"] >= 0.0
#         assert response.json()["similarity"] <= 100.0
