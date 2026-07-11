from random import randint
import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_request = {
        "name": "TestUser",
        "login": f"TestUser-login-{randint(100, 100000000)}"
    }

    response = client.post("/api/v1/users", json=user_request)
    assert response.status_code == 200
    user = response.json()
    
    return {**user_request, **user}


@pytest.fixture
def auth_headers(client, test_user) -> dict:
    return {"Authorization": f"Bearer {test_user["login"]}"}


@pytest.fixture
def test_wallet(client, auth_headers) -> dict:
    def _test_wallet(name, currency):
        wallet_request = {
            "name": name,
            "currency": currency
        }
        response = client.post("/api/v1/wallets", headers=auth_headers, json=wallet_request) 
        assert response.status_code == 200

        return {**wallet_request, **response.json()}
    return _test_wallet



@pytest.fixture
def add_income(client, auth_headers) -> dict:
    def _add_income(wallet_name, amount):
        income_request = {
            "wallet_name": wallet_name,
            "type": "income",
            "amount": amount,
            "description": ""
        }
        response = client.post("/api/v1/operations", headers=auth_headers, json=income_request)
        assert response.status_code == 200

        return {**income_request, **response.json()}
    return _add_income






