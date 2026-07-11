# Just an introduction to pytest and testing in general. Can be ignored for now.

import pytest
from src.building_blocks.errors import BusinessRuleViolationError

operation_test_data = [
    {
        "type": "income",
        "amount": 7.69,
        "description": ""
    },
    {
        "type": "expense",
        "amount": 7,
        "description": ""
    }
]


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user(client):
    response = client.post(
        "/api/v1/users",
        json={"name": "olya",
              "login": "olya-login"})
    
    assert response.status_code == 200
    user_response = response.json()
    assert "id" in user_response
    assert user_response["name"] == "olya"
    assert user_response["login"] == "olya-login"
    

def test_no_auth_on_me(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_auth_on_me(client, test_user):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user["login"]}"}
        )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == test_user["name"]
    assert response.json()["login"] == test_user["login"]


def test_create_wallet_no_auth(client):
    response = client.post(
        "/api/v1/wallets",
        json={"name": "new-wallet",
              "currency": "usd"})
    assert response.status_code == 401


def test_create_wallet_auth(client, test_user):
    response = client.post(
        "/api/v1/wallets",
        headers={"Authorization": f"Bearer {test_user["login"]}"},
        json={"name": "new-wallet",
              "currency": "usd"})
    
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "user_id", "name", "balance", "currency"}
    assert response.json()["user_id"] == test_user["id"]
    assert response.json()["name"] == "new-wallet"
    assert response.json()["currency"] == "usd"


@pytest.mark.parametrize("operation_data", operation_test_data)
def test_create_operation_auth(client, test_user, test_wallet, operation_data):
    operation_request = {"wallet_name": f"{test_wallet['name']}", **operation_data}

    if operation_request["type"] == "income":
        response = client.post(
            "/api/v1/operations",
            headers={"Authorization": f"Bearer {test_user["login"]}"},
            json=operation_request
        )

        assert response.status_code == 200

        assert response.json()["wallet_id"] == test_wallet["id"]
        assert response.json()["destination_id"] == None

        assert response.json()["type"] == operation_request["type"]
        assert response.json()["currency"] == test_wallet["currency"]
        assert response.json()["description"] == operation_request["description"]
    
    elif operation_request["type"] == "expense":
        with pytest.raises(BusinessRuleViolationError):
            response = client.post(
                "/api/v1/operations",
                headers={"Authorization": f"Bearer {test_user["login"]}"},
                json=operation_request
            )


def test_create_transfer_auth(client, test_user):
    wallet1_response = client.post(
            "/api/v1/wallets",
            headers={"Authorization": f"Bearer {test_user["login"]}"},
            json={
                "name": "NewWallet1",
                "currency": "usd"
            })
    assert wallet1_response.status_code == 200
    
    income_response = client.post(
        "/api/v1/operations",
        headers={"Authorization": f"Bearer {test_user["login"]}"},
        json={
            "wallet_name": "NewWallet1",
            "type": "income",
            "amount": 10000,
            "description": ""
        })
    assert income_response.status_code == 200
   
    wallet2_response = client.post(
        "/api/v1/wallets",
        headers={"Authorization": f"Bearer {test_user["login"]}"},
        json={
            "name": "NewWallet2",
            "currency": "eur"
        })
    assert wallet2_response.status_code == 200

    transfer_response = client.post(
        "/api/v1/operations/transfer",
        headers={"Authorization": f"Bearer {test_user["login"]}"},
        json={
            "wallet_name": "NewWallet1",
            "destination_name": "NewWallet2",
            "amount": 10000,
            "description": "Test transfer"
        })
    assert transfer_response.status_code == 200


def test_transfer_auth(client, auth_headers,  test_wallet, add_income, get_balance):
    wallet1 = test_wallet("TestWallet1", "eur")
    income = add_income("TestWallet1", 10000)

    wallet2 = test_wallet("TestWallet2", "usd")

    transfer_request = {
        "wallet_name": wallet1["name"],
        "destination_name": wallet2["name"],
        "amount": 1000,
        "description": ""
    }
    response = client.post("/api/v1/operations/transfer", headers=auth_headers, json=transfer_request)

    assert response.status_code == 200




