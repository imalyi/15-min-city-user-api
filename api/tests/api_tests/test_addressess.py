from httpx import AsyncClient
import pytest

geometry = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [102.0, 2.0],
                [103.0, 2.0],
                [103.0, 3.0],
                [102.0, 3.0],
                [102.0, 2.0],
            ]
        ],
        [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0],
            ]
        ],
    ],
}


@pytest.mark.parametrize(
    "ac, street_name, house_number, street_type, city, postcode, geometry, status_code",
    [
        # Admin successful creation
        (
            "ac_admin",
            "successful creation",
            "12A",
            "Ave",
            "Warsaw",
            "30-123",
            geometry,
            201,
        ),
        # User forbidden to create
        (
            "ac_user",
            "Secondary Street",
            "34B",
            "Blv",
            "Krakow",
            "30-123",
            {"type": "MultiPolygon", "coordinates": [[[]]]},
            403,
        ),
        # Invalid postcode
        (
            "ac_admin",
            "Main Street",
            "12A",
            "Ave",
            "Warsaw",
            "00001",
            geometry,
            422,
        ),
        # Missing postcode
        (
            "ac_admin",
            "Main Street",
            "12A",
            "Ave",
            "Warsaw",
            201,
            geometry,
            422,
        ),
        # Invalid city
        (
            "ac_admin",
            "Main Street",
            "12A",
            "Ave",
            "W@rsaw",
            "00-001",
            geometry,
            422,
        ),
        # Invalid geometry
        (
            "ac_admin",
            "Invalid geometry",
            "12A",
            "Ave",
            "Warsaw",
            "30-123",
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [1042.0, 2.0],
                            [103.0, 2.0],
                            [103.0, 3.0],
                            [102.0, 3.0],
                            [102.0, 2.0],
                        ]
                    ]
                ],
            },
            422,
        ),
        # Valid data but empty street name
        (
            "ac_admin",
            "",
            "12A",
            "Ave",
            "Warsaw",
            "00-001",
            geometry,
            422,
        ),
        # Street name too short
        (
            "ac_admin",
            "A",
            "12A",
            "Ave",
            "Warsaw",
            "00-001",
            geometry,
            422,
        ),
        # Invalid type for house number
        (
            "ac_admin",
            "Main Street",
            123,
            "Ave",
            "Warsaw",
            "00-001",
            geometry,
            422,
        ),
        # Missing required field (street_name)
        (
            "ac_admin",
            None,
            "12A",
            "Ave",
            "Warsaw",
            "00-001",
            geometry,
            422,
        ),
    ],
    indirect=["ac"],
)
async def test_create_address(
    ac,
    street_name,
    house_number,
    street_type,
    city,
    postcode,
    geometry,
    status_code,
):
    data = {
        "street_name": street_name,
        "house_number": house_number,
        "street_type": street_type,
        "city": city,
        "postcode": postcode,
        "geometry": geometry,
    }
    response = await ac.post("/addresses/", json=data)
    assert response.status_code == status_code
