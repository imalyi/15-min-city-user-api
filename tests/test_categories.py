from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from routers.categories import router

client = TestClient(router)


def test_get_categories():
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.json()) > 10
