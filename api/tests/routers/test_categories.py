from httpx import AsyncClient
import pytest


async def create_category(
    parent_category: str, child_category: str, async_client=AsyncClient
) -> dict:
    response = await async_client.post(
        "/categories/",
        json={
            "parent_category": parent_category,
            "child_category": child_category,
        },
    )
    return response.json()


@pytest.fixture()
async def created_category(async_client: AsyncClient):
    response = await create_category(
        "test parent category",
        "test child category",
        async_client=async_client,
    )
    return response


@pytest.mark.anyio
async def test_create_category(async_client: AsyncClient):
    parent_category = "test parent category"
    child_category = "test child category"

    response = await async_client.post(
        "/categories/",
        json={
            "parent_category": parent_category,
            "child_category": child_category,
        },
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "parent_category": parent_category,
        "child_category": child_category,
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_dublicate_categories(
    async_client: AsyncClient, created_category: dict
):
    response = await async_client.post(
        "/categories/",
        json={
            "parent_category": "test parent category",
            "child_category": "test child category",
        },
    )

    assert response.status_code == 409


@pytest.mark.anyio
async def test_get_categories(async_client: AsyncClient):
    response = await async_client.get(
        "/categories/",
    )
    assert response.status_code == 200
