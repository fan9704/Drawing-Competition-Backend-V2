import pytest

from src.main import app
from tests.client import TestClient
from src.models.tortoise import Team

PREFIX = "/api/team"
client = TestClient(PREFIX, app)


@pytest.mark.asyncio
class TestE2ETeam:
    @pytest.mark.asyncio
    async def test_list(self, in_memory_db):
        await Team.create(id=1, name="Team Alpha", token="EFSA")
        await Team.create(id=2, name="Team Beta", token="BCDE")
        response = client.get("/api/team/")
        print(f"\nResponse Body: {response.text}")
        assert response.status_code == 200
