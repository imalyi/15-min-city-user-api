import asyncio
import pytest
from httpx import AsyncClient

# pytest_plugins = ("pytest_asyncio",)


async def test_get_all_category_collections(ac_user):
    response = await ac_user.get("/category-collections/")
    assert response.status_code == 200


# @pytest.mark.parametrize("user, input, expected", [])
# async def test_create_category_collections(ac_admin_user):
#    pass
