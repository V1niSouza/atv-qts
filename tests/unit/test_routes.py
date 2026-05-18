import pytest
from app.services import user_service


@pytest.fixture(autouse=True)
def reset_users():
    user_service.users.clear()
    user_service.current_id = 1


def test_create_user_sucess(client):
    response = client.post("/users", json={"name": "Vini"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Vini"


def test_create_user_without_name(client):
    response = client.post("/users", json={})
    assert response.status_code == 400
    assert "name is required" in str(response.data)


def test_get_user(client):
    client.post("/users", json={"name": "teste"})
    response = client.get("/users/1")
    assert response.status_code == 200


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in str(response.data)


def test_delete_user(client):
    client.post("/users", json={"name": "Delete"})
    response = client.delete("/users/1")
    assert response.status_code == 204


def test_update_user_success(client):
    response = client.post("/users", json={"name": "Vini"})
    assert response.status_code == 201
    user_id = response.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"name": "novo nome"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "novo nome"


def test_should_not_allow_duplicate_users():
    from app.services import user_service

    user_service.users.clear()
    user_service.current_id = 1
    user_service.create_user({"name": "Vini"})
    user = user_service.create_user({"name": "Vini"})
    assert user is None


def test_should_return_400_when_user_already_exists(client):
    client.post("/users", json={"name": "Vini"})
    response = client.post("/users", json={"name": "Vini"})
    assert response.status_code == 400


# NOVOS TESTES UNITÁRIOS
def test_get_all_users_empty():
    assert user_service.get_all_users() == []


def test_create_user_vinicius_souza():
    user = user_service.create_user({"name": "Vinicius Souza"})
    assert user["name"] == "Vinicius Souza"
    assert user["id"] == 1


def test_create_user_vinicius_leal():
    user = user_service.create_user({"name": "Vinicius Leal"})
    assert user["id"] == 1


def test_increment_id_multiple_users():
    user_service.create_user({"name": "Paulo Cesar"})
    user_service.create_user({"name": "João Lima"})
    assert user_service.get_user_by_id(2)["name"] == "João Lima"


def test_get_user_by_id_found():
    user_service.create_user({"name": "Vinicius Souza"})
    user = user_service.get_user_by_id(1)
    assert user["name"] == "Vinicius Souza"


def test_get_user_by_id_not_found():
    assert user_service.get_user_by_id(999) is None


def test_update_user_not_found():
    assert user_service.update_user(999, {"name": "X"}) is None


def test_delete_user_removes_user():
    user_service.create_user({"name": "João Lima"})
    user_service.delete_user(1)
    assert user_service.get_user_by_id(1) is None


def test_duplicate_user_blocked():
    user_service.create_user({"name": "Vinicius Souza"})
    result = user_service.create_user({"name": "Vinicius Souza"})
    assert result is None
