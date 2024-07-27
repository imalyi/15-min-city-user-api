import asyncio
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "ac, count", [("ac_user", 1), ("ac_admin", 2)], indirect=["ac"]
)
async def test_get_all_category_collections(ac, count):
    response = await ac.get("/category-collections/")
    assert response.status_code == 200
    assert len(response.json()[0]["categories"]) == count


@pytest.mark.parametrize(
    "title, synonims, expected_status_code, expected_title_in_response",
    [
        (
            "Valid Collection",
            ["synonym1", "synonym2"],
            201,
            True,
        ),  # Valid case
        (
            "Valid Collection",
            ["synonym1", "duplicate"],
            409,
            False,
        ),  # Duplicating
        ("s", ["synonym1"], 422, False),  # Title too short
        (
            "TitleWith@In$#validChar",
            ["synonym1"],
            422,
            False,
        ),  # Invalid characters in title
        (
            "Another Valid Collection",
            None,
            201,
            True,
        ),  # Valid case with no synonims
        (
            "fail" * 200,
            ["synonym1"],
            422,
            False,
        ),  # Title too long
        (
            "123",
            ["synonym1"],
            422,
            False,
        ),  # Title with non-alphabetic characters
    ],
)
async def test_create_category_collection(
    ac_admin, title, synonims, expected_status_code, expected_title_in_response
):
    response = await ac_admin.post(
        "/category-collections/",
        json={
            "title": title,
            "synonims": synonims,
        },
    )
    assert response.status_code == expected_status_code
    assert ("title" in response.json()) == expected_title_in_response


# Обязательно протестировать создание категории, коллекции категории и возврат данных
# создание адрресаа
# поиск адресса по полям. Поиск ilike. Заодно пофиксить генерацию имён алиасов
