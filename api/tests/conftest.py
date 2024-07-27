import pytest
import asyncio
import logging
from api.addresses.models import Address


import json
from httpx import AsyncClient
from api.api import app as fastapi_app
from sqlalchemy import insert
from api.category_collections.models import CategoryCollections
from api.category_collections.categories.models import Categories
from api.addresses.models import Address
from api.pois.models import POI
from api.pois.categories.models import POICategories
from api.pois.reviews.models import Review
from api.subscriptions.models import SubscriptionLevel
from api.users.models import User
from api.users.subscriptions.models import UserSubscription
from api.invite_codes.models import InviteCode
from api.users.history.models import UserHistory
from api.database import Base, async_session_maker, engine
from datetime import datetime
from httpx import ASGITransport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from sqlalchemy import text


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(event_loop):
    # assert config.ENV_STATE == "test"
    logger.info("Starting database preparation")

    logger.info("Dropping all tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, checkfirst=True)
    logger.info("Creating all tables")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(
            f"api/tests/mock_data/{model}.json", "r", encoding="utf-8"
        ) as f:
            data = json.loads(f.read())

        for record in data:
            if "created_at" in record:
                record["created_at"] = datetime.fromisoformat(
                    record["created_at"]
                )
            if "modified_at" in record:
                record["modified_at"] = datetime.fromisoformat(
                    record["modified_at"]
                )

        return data

    categories = open_mock_json("categories")
    category_collections = open_mock_json("category_collections")
    categories = open_mock_json("categories")
    users = open_mock_json("users")
    async with async_session_maker() as session:
        try:

            add_category_collections = insert(CategoryCollections).values(
                category_collections
            )
            add_categories = insert(Categories).values(categories)
            add_users = insert(User).values(users)
            await session.execute(add_category_collections)
            await session.execute(add_categories)
            await session.execute(add_users)
            await session.commit()
            logger.info("Test data committed to the database")
        except Exception as e:
            logger.error(f"Error occurred whil  e inserting test data: {e}")
            await session.rollback()
            raise

    yield
    logger.info("Cleaning up the database after tests")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Dropped all tables after tests")
    logger.info("Test database cleanup complete")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac_user():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/users/login",
            data={
                "username": "regular.user@example.com",
                "password": "password12341!",
            },
        )
        assert "access_token" in response.json()
        access_token = response.json()["access_token"]
        ac.headers.update({"Authorization": f"Bearer {access_token}"})
        yield ac


@pytest.fixture(scope="session")
async def ac_admin():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/users/login",
            data={
                "username": "admin.user@example.com",
                "password": "password12341!",
            },
        )
        assert "access_token" in response.json()
        access_token = response.json()["access_token"]
        ac.headers.update({"Authorization": f"Bearer {access_token}"})
        yield ac


@pytest.fixture
async def ac(request, ac_user, ac_admin):
    if request.param == "ac_admin":
        yield ac_admin
    elif request.param == "ac_user":
        yield ac_user
    else:
        raise ValueError("Unknown ac fixture parameter")
