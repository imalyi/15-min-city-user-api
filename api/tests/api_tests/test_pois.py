import pytest


@pytest.mark.parametrize(
    "ac, name, data, address_id, expected_status",
    [
        ("ac_admin", "Test ADmin POI", {"key": "value"}, 1, 201),
        ("ac_admin", "Another  admin POI no data", None, 1, 201),
        (
            "ac_admin",
            "",
            {"key": "value"},
            1,
            422,
        ),
        ("ac_admin", "Valid POI", {"invalid": "data"}, 1, 201),
        ("ac_user", "User POI", {"key": "value"}, 1, 403),
        ("ac_user", "Another User POI", None, 1, 403),
    ],
    indirect=["ac"],
)
async def test_create_poi(ac, name, data, address_id, expected_status):
    payload = {"name": name, "address_id": address_id}
    if data is not None:
        payload["data"] = data
    response = await ac.post("/pois/", json=payload)
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["name"] == name
        #        assert response.json()["address_id"] == address_id
        if data:
            assert response.json()["data"] == data
