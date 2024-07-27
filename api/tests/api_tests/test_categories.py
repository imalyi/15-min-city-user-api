from httpx import AsyncClient
import pytest
from api.tests.conftest import ac_user, ac_admin


@pytest.mark.parametrize(
    "ac, status_code", [("ac_user", 403), ("ac_admin", 200)], indirect=["ac"]
)
async def test_get_all_categories(ac, status_code):
    response = await ac.get("/categories/")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "ac, title, collection_id, is_default, is_hidden, order, minimum_subscription_level,status_code",
    [
        # Admin successful creation
        ("ac_admin", "Admin Category", 1, True, False, 1, 1, 201),
        # User forbidden to create
        ("ac_user", "New Category", 1, False, False, 0, 1, 403),
        # Empty title (validation error)
        ("ac_admin", "", 1, True, False, 1, 1, 422),
        # Title too short (validation error)
        ("ac_admin", "A", 1, True, False, 1, 1, 422),
        # Title with invalid characters (validation error)
        ("ac_admin", "Category1", 1, True, False, 1, 1, 422),
        # Missing collection_id (validation error)
        ("ac_admin", "Valid Title", None, True, False, 1, 1, 422),
        # Invalid type for collection_id (validation error)
        ("ac_admin", "Valid Title", "invalid_id", True, False, 1, 1, 422),
        # Invalid type for is_default (validation error)
        ("ac_admin", "Valid Title", 1, "not_a_boolean", False, 1, 1, 422),
        # Invalid type for is_hidden (validation error)
        ("ac_admin", "Valid Title", 1, True, "not_a_boolean", 1, 1, 422),
        # Invalid type for order (validation error)
        ("ac_admin", "Valid Title", 1, True, False, "not_an_int", 1, 422),
    ],
    indirect=["ac"],
)
async def test_create_category(
    ac,
    title,
    collection_id,
    is_default,
    is_hidden,
    order,
    minimum_subscription_level,
    status_code,
):
    data = {
        "title": title,
        "collectionId": collection_id,
        "isDefault": is_default,
        "isHidden": is_hidden,
        "order": order,
        "minimum_subscription_level": minimum_subscription_level,
    }
    response = await ac.post("/categories/", json=data)
    assert response.status_code == status_code
