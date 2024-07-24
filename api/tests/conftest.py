import pytest
from api.database import Base, async_session_maker, engine
from api.config import config
import asyncio
import logging

from api.addresses.models import Address
from api.category_collections.categories.models import Categories
from api.category_collections.models import CategoryCollections

import json
from fastapi.testclient import TestClient
from httpx import AsyncClient
from api.api import app as fastapi_app
from api.category_collections.models import CategoryCollections
from api.category_collections.categories.models import Categories
from sqlalchemy import insert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
async def prepare_database():
    assert config.ENV_STATE == "test"
    logger.info("Starting database preparation")

    logger.info("Dropping all tables")
    Base.metadata.drop_all(engine)
    logger.info("Creating all tables")
    # Base.metadata.create_all(engine)

    def open_mock_json(model: str):
        with open(
            f"api/tests/mock_data/{model}.json", "r", encoding="utf-8"
        ) as f:
            return json.loads(f.read())

    categories = open_mock_json("categories")
    async with async_session_maker() as session:
        try:
            add_categories = insert(Categories).values(categories)
            await session.execute(add_categories)
            await session.commit()
            logger.info("Test data committed to the database")
        except Exception as e:
            logger.error(f"Error occurred while inserting test data: {e}")
            await session.rollback()
            raise

    yield
    logger.info("Test database setup complete")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac(event_loop):
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def ac_user(event_loop):
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/users/register",
            json={
                "email": "testuser@test.com",
                "password": "password12341!",
                "name": "supername",
            },
        )
        response = await ac.post(
            "/users/login",
            data={
                "username": "testuser@test.com",
                "password": "password12341!",
            },
        )
        assert "access_token" in response.json()
        yield ac


@pytest.fixture(scope="session")
async def ac_admin(event_loop):
    pass
