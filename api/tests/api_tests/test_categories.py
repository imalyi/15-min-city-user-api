from httpx import AsyncClient


async def test_get_all_categories_user(ac_user, prepare_database):
    # response = await ac_user.get("/categories")
    # assert len(response.json()) > 0
    pass


async def test_get_all_categories_admin(ac_admin):
    pass


async def create_category(ac_admin):
    pass


async def get_category_by_id(ac_admin):
    pass
