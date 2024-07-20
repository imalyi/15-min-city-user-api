import pytest
from api.database import Base, async_session_maker, engine
from api.config import config
import asyncio

from api.addresses.models import Address
from api.categories.models import Categories
from api.category_collections.models import CategoryCollections

import json
from fastapi.testclient import TestClient
from httpx import AsyncClient
from api.api import app as fastapi_app


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert config.ENV_STATE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open("api/tests/mock/{model}.json", "r") as f:
            return json.load(f)


#    addresses = open_mock_json("addresses")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="htpp://test") as ac:
        yield ac
