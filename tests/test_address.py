from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from routers.address import router

client = TestClient(router)


def test_get_address_by_partial_name():
    response = client.get('/?name=Seweryna Goszczyńskiego 17, Gdańsk')
    assert response.status_code == 200
    assert response.json()[0] == 'Seweryna Goszczyńskiego 17, Gdańsk'


def test_get_not_existing_address_by_partial_name():
    with pytest.raises(HTTPException) as err:
        response = client.get('/?name=NOT_EXIST')
        assert response.status_code == 404

