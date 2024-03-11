from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from routers.report import router

client = TestClient(router)


def test_get_report_for_existing_address():
    response = client.get('/?address=Seweryna Goszczyńskiego 17, Gdańsk&cat=sauny')
    assert response.status_code == 200


def test_get_report_for_non_existing_address():
    with pytest.raises(HTTPException) as err:
        response = client.get('/?address=NOT_EXIST&cat=sauny')
        assert response.status_code == 404
