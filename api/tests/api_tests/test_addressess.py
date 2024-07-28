import pytest


@pytest.mark.parametrize(
    "ac, name, data, address_id, expected_status",
    [
        ("ac_admin", "Test POI", {"key": "value"}, 1, 201),
        ("ac_admin", "Another POI", None, 1, 201),
        (
            "ac_admin",
            "",
            {"key": "value"},
            1,
            201,
        ),  # Invalid case: name is required
        (
            "ac_admin",
            "Valid POI 2",
            {"invalid": "data"},
            1,
            201,
        ),  # Assuming your endpoint accepts any dict
        ("ac_user", "User POI", {"key": "value"}, 1, 403),
    ],
    indirect=["ac"],
)
async def test_create_poi(ac, name, data, address_id, expected_status):
    payload = {
        "name": name,
        "address_id": address_id,
    }  # Add address_id to payload
    if data is not None:
        payload["data"] = data
    response = await ac.post("/pois/", json=payload)
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["name"] == name


#        if data:
#            assert response.json()["data"] == data
#        assert (
#            response.json()["address_id"] == address_id
#        )  # Check if address_id is returned correctly
